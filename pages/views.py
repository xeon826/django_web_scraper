from django.views.generic import TemplateView
from .models import Item, ItemStatus
from accounts.models import CustomUser
import validators
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from google_images_search import GoogleImagesSearch
import os
from dotenv import load_dotenv
from django.contrib.auth.signals import user_logged_out
from django.core.paginator import Paginator
from django.shortcuts import render
from .forms import IndexForm


def logged_out(sender, **kwargs):
    user = kwargs['user']
    item = Item.objects.filter(status='Processing', assigned_to=user).first()
    if item is not None:
        item.status = ItemStatus.objects.filter(title='Unprocessed').first()
        item.assigned_to = None
        item.save()
        print('Changed item status')


user_logged_out.connect(logged_out)


class HomePageView(TemplateView):
    template_name = "pages/home.html"


class ImportItemListPageView(TemplateView):
    template_name = "pages/import_item_list.html"


def parse_item_file(request, template_name='pages/parse_item_file.html'):
    item_list = request.FILES['item-list']
    file_extension = os.path.splitext(item_list.name)[1]
    if file_extension.lower() != '.txt':
        return redirect(request.META.get('HTTP_REFERER'))
    item_list_content = item_list.read()
    items = item_list_content.decode('utf-8').splitlines()
    objects = []
    for item in items:
        obj = Item()
        obj.name = item
        obj.status = ItemStatus.objects.get(pk=1)
        objects.append(obj)
    Item.objects.bulk_create(objects)
    item_list.close()
    return redirect('item_identify')


def item_identify(request, template_name="pages/item_identify.html"):
    user = CustomUser.objects.get(pk=request.user.id)
    item = Item.objects.filter(status='Processing', assigned_to=user).first()
    if 'item_id' in request.GET:
        if item != None:
            item.assigned_to = None
            item.status = ItemStatus.objects.filter(
                title='Unprocessed').first()
            item.save()
        item = Item.objects.filter(pk=request.GET['item_id']).first()
        item.status = ItemStatus.objects.filter(title='Processing').first()
        item.assigned_to = user
        item.save()
    unprocessed_item = Item.objects.filter(status__title='Unprocessed').first()
    args = {}
    if item is None and unprocessed_item is None:
        args['have_items'] = False
        return TemplateResponse(request, template_name, args)
    else:
        args['have_items'] = True
    if item is None:
        item = unprocessed_item
        item.status = ItemStatus.objects.filter(title='Processing').first()
        item.assigned_to = user
        item.save()
    image_list = []
    image_list = get_image_results(item.name, user.gis_validation, user)
    args['image_list'] = image_list
    args['item'] = item
    if 'return_to_index' in request.GET:
        args['return_to_index'] = True
    return TemplateResponse(request, template_name, args)


def get_image_results(item_name, gis_validation=False, user=''):
    load_dotenv()
    gis = GoogleImagesSearch(os.environ['GAPI_KEY'],
                             os.environ['PROJECT_CX'],
                             validate_images=gis_validation)
    gis.search(
        search_params={
            'q':
            item_name,
            'num':
            user.items_per_grid if gis_validation else user.items_per_grid +
            15,
            'fileType':
            'jpg|gif|png'
        })
    image_list = gis.results() if gis_validation else validate_images(
        gis.results(), user)
    return image_list


def validate_images(image_list, user):
    result = []
    for image in image_list:
        if not validators.url(image.url):
            continue
        result.append(image)
        if len(result) >= user.items_per_grid:
            break
    return result


def item_identify_save(request):
    item = Item.objects.get(pk=request.POST['item_id'])
    item.url = request.POST['img_url']
    item.status = ItemStatus.objects.filter(title='Processed').first()
    item.save()
    if request.POST['return_to_index']:
        return redirect('item_index')
    return redirect(request.META.get('HTTP_REFERER'))


def item_skip(request):
    item = Item.objects.get(pk=request.GET['item_id'])
    item.status = ItemStatus.objects.filter(title='Processed').first()
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


def unprocess(request):
    item = Item.objects.get(pk=request.GET['item_id'])
    item.assigned_to = None
    item.url = None
    item.status = ItemStatus.objects.filter(title='Unprocessed').first()
    item.save()
    return redirect(request.META.get('HTTP_REFERER'))


def settings(request, template_name="pages/settings.html"):
    # user = CustomUser.objects.get(pk=request.user.id)
    user = CustomUser.objects.get(**{'pk': request.user.id})
    if request.method == 'POST':
        user.gis_validation = bool(request.POST.get('gis_validation', ''))
        user.items_per_grid = int(request.POST.get('items_per_grid', ''))
        user.save()
    args = {}
    args['user'] = user
    return TemplateResponse(request, template_name, args)


def item_index(request, template_name='pages/item_index.html'):
    args = {}
    item_list = Item.objects.all()
    form = IndexForm(request.GET)
    args['form'] = form
    if 'form_submitted' in request.GET and form.is_valid():
        item_list = Item.objects.filter(
            **{k: v
               for k, v in form.cleaned_data.items() if v}).all()
    else:
        item_list = Item.objects.all()
    args['item_statuses'] = ItemStatus.objects.all()
    paginator = Paginator(item_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    args['page_obj'] = page_obj
    return TemplateResponse(request, template_name, args)
