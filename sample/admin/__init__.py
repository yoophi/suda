#!/usr/bin/env python
# coding: utf-8
from flask.ext.admin.form import rules
from flask.ext.debugtoolbar import DebugToolbarExtension

import os

from jinja2 import Markup
from flask import Flask, url_for
from flask.ext.babelex import Babel, Domain
from flask_sqlalchemy import SQLAlchemy
from flask_admin.contrib import sqla
import flask_admin
from flask_admin import form

from delivery import config
from delivery.models import (
    User, UserInfo, Restaurant, MenuGroup, Menu, Category,
    RestaurantMeta, MenuOption, MenuPrice, MenuChoice, Cart,
    Order, OrderItem, OrderInfo, OrderPayment, RestaurantMedia,
    Review, Event, Notice, Faq, Inquiry, Term, GuestUser,
    CeoUser, AppVersion)

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')

debug_toolbar = DebugToolbarExtension()

app = Flask(__name__, template_folder=tmpl_dir, )
app.secret_key = 'SECRET'
app.debug = True

debug_toolbar.init_app(app)
config.init(app, os.getenv('FLASK_CONFIG') or 'default')

db = SQLAlchemy(app)

file_path = os.path.join(os.path.dirname(__file__), 'static', 'category_images')
try:
    os.mkdir(file_path)
except OSError:
    pass


# Initialize babel
babel = Babel(app, default_locale='ko')


@babel.localeselector
def get_locale():
    return 'ko'


def _str_list_to_ul(view, context, model, name):
    return Markup('<ul>%s</ul>' % (
        ''.join(map('<li>{}</li>'.format, getattr(model, name).split('|'))),))


def _view_img(view, context, model, name):
    # 이미지 출력
    image = getattr(model, name)
    return Markup('<img src="%s" width="40">' % image) \
        if image else ''


def _cut_date(view, context, model, name):
    return getattr(model, name).strftime('%Y-%m-%d %H:%M')


class MyModelView(sqla.ModelView):
    can_view_details = True

    column_formatters = {
        'created_at': _cut_date,
        'updated_at': _cut_date,
        'image_url': _view_img,
    }

    # def get_save_return_url(self, model, is_created):
    #    return self.get_url('.details_view', id=model.id)


class UserAdmin(sqla.ModelView):
    column_list = ['name', 'status', 'terms_approval_date']
    column_exclude_list = ['_password']


class GuestUserAdmin(sqla.ModelView):
    column_list = ['user_uuid', 'device_id', 'is_expired']
    column_exclude_list = ['_password']


class UserInfoAdmin(sqla.ModelView):
    column_sortable_list = ('user_id', '_registered_date')


class CategoryAdmin(MyModelView):
    form_excluded_columns = ('created_at', 'updated_at')
    column_list = ('name', 'image_url', 'created_at', 'updated_at', 'order')
    column_searchable_list = ['name']

    form_extra_fields = {
        'image_path': form.ImageUploadField('Image',
                                            base_path=file_path,
                                            thumbnail_size=(100, 100, True))
    }


class RestaurantAdmin(MyModelView):
    # meta flask_admin 버그인듯
    form_excluded_columns = ('meta', 'created_at', 'updated_at', 'menu_groups', 'menus', 'media', 'reviews', 'orders')
    column_list = ('name', 'created_at', 'updated_at')
    # edit_template = 'admin/restaurant_edit.html'
    # list_template = 'admin/restaurant_list.html'


class RestaurantMetaAdmin(sqla.ModelView):
    # column_sortable_list = ('user_id', '_registered_date')
    pass


class MenuGroupAdmin(sqla.ModelView):
    # column_sortable_list = ('user_id', '_registered_date')
    pass


class MenuAdmin(sqla.ModelView):
    # column_sortable_list = ('user_id', '_registered_date')
    pass


class MenuOptionAdmin(sqla.ModelView):
    column_formatters = {
        'names': _str_list_to_ul,
        'prices': _str_list_to_ul
    }

    form_extra_fields = {}


class CeoUserAdmin(sqla.ModelView):
    # column_exclude_list = ['password']
    column_list = ['username', 'name', 'created_at', 'updated_at']
    form_columns = ['username', 'name', 'password']


class AppVersionAdmin(sqla.ModelView):
    breadcrumb = (
        (None, '서비스 관리'),
        ('appversion.index_view', '버전 관리'),
    )

    list_template = 'admin/list.html'
    create_template = 'admin/create.html'
    edit_template = 'admin/edit.html'

    service_types = AppVersion.service_types

    @property
    def form_choices(self):
        return {
            'service_type': self.service_types
        }

    column_exclude_list = ('created_at', 'updated_at')

    column_labels = {
        'service_type': '서비스',
        'is_force_update': '강제업데이트 여부',
        'apply_version': '적용 버전',
        'update_adtv': '멸치TV 업데이트',
        'update_delivery': '멸치배달 업데이트',
        'content': '업데이트 내용',
    }

    column_descriptions = {
        # 'is_force_update': '체크하면 강제업데이트로 설정됩니다.'
    }

    form_excluded_columns = ('created_at', 'updated_at')

    form_create_rules = (
        'service_type',
        'apply_version',
        'is_force_update',
        'update_adtv',
        'update_delivery',
        'content',
    )

    form_edit_rules = form_create_rules


    def _list_service_type(self, content, model, name):
        service_types = dict(self.service_types)
        return Markup('<a href="%s">%s</a>' % (
            url_for('appversion.index_view', flt1_0=model.service_type),
            service_types.get(str(model.service_type))
        ))

    def _list_content(self, content, model, name):
        if not model.content:
            return ''

        return Markup('<pre>%s</pre>' % (model.content,))

    column_formatters = {
        'service_type': _list_service_type,
        'content': _list_content
    }

    column_filters = ('service_type',)


admin = flask_admin.Admin(app, name='멸치배달관리', template_mode='bootstrap3',
                          translations_path=os.path.join(os.path.dirname(__file__), 'translations'))

# 서비스 관리
admin.add_view(AppVersionAdmin(AppVersion, db.session, name='버전 관리', category='서비스 관리'))

admin.add_view(UserAdmin(User, db.session, name="회원", category='사용자'))
admin.add_view(UserInfoAdmin(UserInfo, db.session, name="사용자 정보", category='사용자'))
admin.add_view(GuestUserAdmin(GuestUser, db.session, name="게스트", category='사용자'))

admin.add_view(CategoryAdmin(Category, db.session, name='음식점분류', category="음식점"))
admin.add_view(RestaurantAdmin(Restaurant, db.session, name='음식점', category="음식점"))
admin.add_view(RestaurantMetaAdmin(RestaurantMeta, db.session, name="기타정보", category='음식점'))
admin.add_view(RestaurantMetaAdmin(RestaurantMedia, db.session, name="사진 및 동영상", category='음식점'))
admin.add_view(RestaurantMetaAdmin(Review, db.session, name="리뷰", category='음식점'))

admin.add_view(MenuGroupAdmin(MenuGroup, db.session, name="메뉴분류", category='메뉴'))
admin.add_view(MenuAdmin(Menu, db.session, name='메뉴', category='메뉴'))
admin.add_view(MenuOptionAdmin(MenuChoice, db.session, name='선택', category='메뉴'))
admin.add_view(MenuOptionAdmin(MenuOption, db.session, name='옵션', category='메뉴'))
admin.add_view(MenuOptionAdmin(MenuPrice, db.session, name='가격', category='메뉴'))

admin.add_view(sqla.ModelView(Cart, db.session, name='장바구니'))

admin.add_view(sqla.ModelView(Order, db.session, name='주문', category='주문'))
admin.add_view(sqla.ModelView(OrderItem, db.session, name='상세', category='주문'))
admin.add_view(sqla.ModelView(OrderInfo, db.session, name='정보', category='주문'))
admin.add_view(sqla.ModelView(OrderPayment, db.session, name='결제', category='주문'))


class EventView(MyModelView):
    column_formatters = {
        'created_at': _cut_date,
        'updated_at': _cut_date,
        'image_url': _view_img,
    }
    column_list = ('type', 'title', 'image_url', 'content_url', 'created_at',
                   'updated_at', 'start_at', 'expire_at')
    form_excluded_columns = ('created_at', 'updated_at')


admin.add_view(EventView(Event, db.session, name='이벤트', category='기타'))


class NoticeView(MyModelView):
    column_formatters = {
        'created_at': _cut_date,
        'updated_at': _cut_date,
        'image_url': _view_img,
    }
    column_list = ('title', 'image_url', 'content_url', 'action', 'created_at',
                   'updated_at',)
    form_excluded_columns = ('created_at', 'updated_at')


admin.add_view(NoticeView(Notice, db.session, name='공지', category='기타'))
admin.add_view(sqla.ModelView(Faq, db.session, name='FAQ', category='기타'))
admin.add_view(sqla.ModelView(Inquiry, db.session, category='기타', name="고객 문의"))
admin.add_view(sqla.ModelView(Term, db.session, category='기타', name="약관"))

admin.add_view(CeoUserAdmin(CeoUser, db.session, name="점주"))


# Flask views
@app.route('/')
def index():
    return '<a href="/admin/">Click me to get to Admin!</a>'


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9000)
