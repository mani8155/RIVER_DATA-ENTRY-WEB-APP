from django.urls import path
from . import views, ward_region, taluk, list_type, list_of_values, town, street, cadastral_entry, \
    cadastral_master, block, intrusion
from .usermanegement import *
from .settings_views import *

urlpatterns = [

    path('home/', ward_region.get_all_ward_data, name="ward-all-data"),
    path('ward_region_form/', ward_region.new_ward_entry, name="ward-form"),
    path('edit_ward_region_form/<int:id>/', ward_region.edit_ward_entry, name="edit-ward-form"),
    path('delete_ward_region/<int:id>/', ward_region.delete_ward_entry, name="delete-ward"),

    path('taluk_list/', taluk.taluk_list, name="taluk-list"),
    path('taluk_form/', taluk.new_taluk_entry, name="taluk-form"),
    path('edit_taluk_form/<int:id>/', taluk.edit_taluk_entry, name="edit-taluk-form"),
    path('delete_taluk/<int:id>/', taluk.delete_taluk_entry, name="delete-taluk"),

    path('list_type/', list_type.get_all_type, name="list-type"),
    path('list_type_form/', list_type.new_type_entry, name="type-form"),
    # path('edit_list_type/<int:id>/', list_type.edit_list_type, name="edit-list-type"),
    # path('delete_type_list/<int:id>/', list_type.delete_list_type, name="delete-list-type"),

    path('list_all_values/', list_of_values.get_all_values, name="list-of-values"),
    path('list_values_form/', list_of_values.new_list_of_values_entry, name="list-value-form"),
    path('edit_list_values/<int:id>/', list_of_values.edit_list_of_values, name="edit-list-value"),
    path('delete_list_values/<int:id>/', list_of_values.delete_list_of_values, name="delete-list-values"),
    path('search_values/', list_of_values.search_values, name="search_values"),

    path('list_of_town/', town.town_master_list, name="list-of-town"),
    path('town_form/', town.new_town_entry, name="town-form"),
    path('edit_town_form/<int:id>/', town.edit_town_entry, name="edit-town-form"),
    path('delete_town/<int:id>/', town.delete_town, name="delete-town"),
    path('get_ward/', town.get_ward, name="get_ward"),

    path('list_of_street/', street.get_all_street_data, name="list-of-street"),
    path('street_form/', street.new_street_entry, name="street-form"),
    path('get_block_details/', street.get_block_details, name='get_block_details'),
    path('edit_street_form/<int:id>/', street.edit_street_entry, name="edit-street-form"),
    path('delete_street/<int:id>/', street.delete_street_entry, name="delete-street"),
    path('street_form_json/', street.street_form_json, name="street_form_json"),
    path('edit_street_form_json/', street.edit_street_form_json, name="edit_street_form_json"),

    path('list_of_cadastal/', cadastral_entry.get_all_cadastral_entry, name="list-of-cadastral"),
    path('cadastal_form/', cadastral_entry.new_cadastral_entry, name="cadastal-form"),
    path('get_town_details_1/', cadastral_entry.get_town_details_1, name='get_town_details_1'),
    path('get_street_base/', cadastral_entry.get_street_base, name='get_street_base'),
    path('get_cadastral_pillar/', cadastral_entry.get_cadastral_pillar, name='get_cadastral_pillar'),
    path('edit_cadastral_form/<int:id>/', cadastral_entry.edit_cadastral_entry, name="edit-cadastral-form"),
    path('delete_cadastral/<int:id>/', cadastral_entry.delete_cadastral_entry, name="delete-cadastral"),
    path('photos_upload/<int:id>/', cadastral_entry.photos_upload, name="photos_upload"),
    path('edit_cadastral_pillar_json/', cadastral_entry.edit_cadastral_pillar_json, name="edit_cadastral_pillar_json"),
    path('get_blocks_for_river/', cadastral_entry.get_blocks_for_river, name="get_blocks_for_river"),
    path('cn_delete_image/<int:parent_id>/<int:id>/', cadastral_entry.cn_delete_image, name="cn_delete_image"),

    path('cadastal_master/', cadastral_master.cadastralmaster_entrys, name="cadastral-master"),
    path('cadastalmaster_form/', cadastral_master.new_cadastralmaster_entry, name="cadastal-master-form"),
    path('edit_cadastralmaster_form/<int:id>/', cadastral_master.edit_cadastramaster_entry,
         name="edit-cadastral-master-form"),
    path('delete_cadastral_master/<int:id>/', cadastral_master.delete_cadastral_master, name="delete-cadastral-master"),
    path("fileupload_master/", cadastral_master.file_upload_master, name="fileupload_master"),
    path("block_use_get_data/", cadastral_master.block_use_get_data, name="block_use_get_data"),
    path("edit_cadastramaster_form_json/", cadastral_master.edit_cadastramaster_form_json, name="edit_cadastramaster_form_json"),

    path("deviation_list/", views.cadastral_deviation_list, name="deviation-list"),
    path("cadastral_deviation_form", views.cadastral_deviation_form, name="cadastral-deviation-form"),
    path("block_no_list/", views.cadastral_entry_block_value, name="block-no"),
    path("get_cadastral/", views.get_cadastral_value, name="get_cadastral"),
    path("get_cadastral_entry/", views.get_cadastral_entry, name="get_cadastral_entry"),
    path("block_no_autofill/", views.block_no_click_autofill, name="block_no_autofill"),
    path("edit_cadastral_deviation/<int:id>/", views.edit_cadastral_deviation, name="edit_cadastral_deviation"),
    path("edit_cadastral_deviation_json/", views.edit_cadastral_deviation_json, name="edit_cadastral_deviation_json"),

    path("delete_cadastral_deviation/<int:id>/", views.delete_cadastral_deviation, name="delete_cadastral_deviation"),
    path("fileupload_deviation/<int:id>/", views.file_upload, name="fileupload_deviation"),

    path('sub_cadastal_line/', cadastral_master.sub_cadastal_line, name="sub_cadastal_line"),
    path('get_ward_cadastral_master/', cadastral_master.get_ward_cadastral_master, name="get_ward_cadastral_master"),
    path('longitude_get_data/', cadastral_master.longitude_get_data, name="longitude_get_data"),

    path('block_lists/', block.get_all_block_data, name="block-lists"),
    path('block_form/', block.block_form, name="block-form"),
    path('block_edit_form/<int:id>/', block.block_edit_entry, name="block-edit-form"),
    path('delete_block/<int:id>/', block.delete_block, name="delete-block"),
    path('get_block/', block.get_town_data, name="get_block"),




    # testing

    path('exit_form/', street.exit_form, name='exit_form'),
    path('new_street_form/', street.street_form, name='new_street_form'),
    path('edit_parent_street/<int:id>/', street.edit_parent_street, name='edit_parent_street'),
    path('child_stree_form/<int:id>/', street.child_stree_form, name='child_stree_form'),
    path('child_street_edit/<int:id>/<int:parent_id>/', street.child_street_edit, name='child_street_edit'),
    path('delete_child_street/<int:id>/<int:parent_id>/', street.delete_child_street, name='delete_child_street'),
    path('new_street_edit/<int:id>/', street.new_street_edit, name='new_street_edit'),


    # enchrochment

    path('child_enchrochment_form/<int:id>/', views.child_enchrochment_form, name='child_enchrochment_form'),
    path('child_enchrochment_edit/<int:id>/<int:parent_id>/', views.child_enchrochment_edit, name='child_enchrochment_edit'),
    path('delete_child_enchrochment/<int:id>/<int:parent_id>/', views.delete_child_enchrochment, name='delete_child_enchrochment'),
    path('edit_parent_enchrochment/<int:id>/', views.edit_parent_enchrochment, name='edit_parent_enchrochment'),
    path('ench_exit_form/', views.exit_form, name='ench_exit_form'),
    path('new_enchrochment_edit/<int:id>/', views.new_enchrochment_edit, name='new_enchrochment_edit'),
    path('get_point_id/', views.get_point_id, name="get_point_id"),


    # Cadastral Line

    path('new_cm_form/', cadastral_master.new_cm_form, name='new_cm_form'),
    path('get_cm_river_value/', cadastral_master.get_cm_river_value, name='get_cm_river_value'),
    path('get_cm_subbassin_value/', cadastral_master.get_cm_subbassin_value, name='get_cm_subbassin_value'),
    path('get_cm_dist_value/', cadastral_master.get_cm_dist_value, name='get_cm_dist_value'),
    path('get_cm_taluk_value/', cadastral_master.get_cm_taluk_value, name='get_cm_taluk_value'),
    path('get_cm_town_value/', cadastral_master.get_cm_town_value, name='get_cm_town_value'),
    # path('edit_cm_jquery/', cadastral_master.edit_cm_jquery, name='edit_cm_jquery'),
    path('child_cm_master_form/<int:id>/', cadastral_master.child_cm_master_form,name='child_cm_master_form'),
    path('child_new_cm_edit/<int:id>/<int:parent_id>/', cadastral_master.child_new_cm_edit,name='child_new_cm_edit'),
    path('delete_new_cm_child/<int:id>/<int:parent_id>/', cadastral_master.delete_new_cm_child,name='delete_new_cm_child'),
    path('edit_parent_new_cm/<int:id>/', cadastral_master.edit_parent_new_cm, name='edit_parent_new_cm'),
    path('new_cm_edit/<int:id>/', cadastral_master.new_cm_edit, name='new_cm_edit'),
    path('exit_new_cm/', cadastral_master.exit_new_cm, name='exit_new_cm'),




    path('get_street_value/', cadastral_entry.get_street_value, name='get_street_value'),
    path('get_survey_no/', cadastral_entry.get_survey_no, name='get_survey_no'),
    path('get_lat_no/', cadastral_entry.get_lat_no, name='get_lat_no'),
    path('get_CEntry_town_value/', cadastral_entry.get_CEntry_town_value, name='get_CEntry_town_value'),
    path('get_CEntry_block_value/', cadastral_entry.get_CEntry_block_value, name='get_CEntry_block_value'),
    path('new_CEntry_edit/<int:id>/', cadastral_entry.new_CEntry_edit, name='new_CEntry_edit'),

    path('get_En_survey_no/', views.get_En_survey_no, name='get_En_survey_no'),
    path('enchrochment2/<int:id>/', views.enchrochment2, name='enchrochment2'),
    path('child_enchrochment_edit_2/<int:id>/<int:parent_id>/', views.child_enchrochment_edit_2, name='child_enchrochment_edit_2'),

    path('st_search_values/', street.st_search_values, name="st_search_values"),
    path('cm_search_values/', cadastral_master.cm_search_values, name="cm_search_values"),
    path('li_search_values/', list_type.li_search_values, name="li_search_values"),
    path('ce_search_values/', cadastral_entry.ce_search_values, name="ce_search_values"),
    path('cd_search_values/', views.cd_search_values, name="cd_search_values"),

    path('intrusion_list/', intrusion.intrusion_list, name="intrusion_list"),
    path('intrusion_form/', intrusion.intrusion_form, name="intrusion_form"),
    path('intrusion_search_values/', intrusion.intrusion_search_values, name="intrusion_search_values"),
    path('intrusion_exit_form/', intrusion.intrusion_exit_form, name="intrusion_exit_form"),
    path('edit_parent_intrusion/<int:id>/', intrusion.edit_parent_intrusion, name="edit_parent_intrusion"),
    path('delete_intrusion/<int:id>/', intrusion.delete_intrusion, name="delete_intrusion"),
    path('child_intrusion_form/<int:id>/', intrusion.child_intrusion_form, name="child_intrusion_form"),
    path('child_intrusion_form2/<int:id>/', intrusion.child_intrusion_form2, name="child_intrusion_form2"),
    path('child_intrusion_edit/<int:id>/<int:parent_id>/', intrusion.child_intrusion_edit,
         name='child_intrusion_edit'),
    path('child_intrusion_edit_2/<int:id>/<int:parent_id>/', intrusion.child_intrusion_edit_2,
         name='child_intrusion_edit_2'),
    path('delete_child_intrusion/<int:id>/<int:parent_id>/', intrusion.delete_child_intrusion,
         name='delete_child_intrusion'),

    path('list_of_values_excel/', list_of_values.list_of_values_excel, name="list_of_values_excel"),
    path('street_excel/', street.street_excel, name="street_excel"),
    path('cadastral_excel/', cadastral_master.cadastral_excel, name="cadastral_excel"),
    path('cadastral_entry_excel/', cadastral_entry.cadastral_entry_excel, name="cadastral_entry_excel"),
    path('enchrochment_excel/', views.enchrochment_excel, name="enchrochment_excel"),
    path('intrusion_excel/', intrusion.intrusion_excel, name="intrusion_excel"),

    path('cl_kml_list/', cadastral_master.cl_kml_list, name="cl_kml_list"),
    path('cl_kml_edit/<int:id>/', cadastral_master.cl_kml_edit, name="cl_kml_edit"),
    path('cl_kml_delete/<int:id>/', cadastral_master.cl_kml_delete, name="cl_kml_delete"),
    path('cl_kml_search_values', cadastral_master.cl_kml_search_values, name="cl_kml_search_values"),

    path('sample_excel_lov/', list_of_values.sample_excel_list_of_values, name="sample_excel_lov"),
    path('sample_excel_street/', street.sample_excel_street, name="sample_excel_street"),
    path('sample_excel_CL/', cadastral_master.sample_excel_CL, name="sample_excel_CL"),
    path('sample_excel_BP/', cadastral_entry.sample_excel_BP, name="sample_excel_BP"),
    path('sample_excel_ench/', views.sample_excel_ench, name="sample_excel_ench"),
    path('sample_excel_intr/', intrusion.sample_excel_intr, name="sample_excel_intr"),

    path('ench_kml_list/', views.ench_kml_list, name="ench_kml_list"),
    path('kml_file_upload_ench/', views.kml_file_upload_ench, name="kml_file_upload_ench"),
    path('ench_kml_edit/<int:id>/', views.ench_kml_edit, name="ench_kml_edit"),
    path('ench_kml_delete/<int:id>/', views.ench_kml_delete, name="ench_kml_delete"),

    path('intrusion_kml_list/', intrusion.intrusion_kml_list, name="intrusion_kml_list"),
    path('kml_file_upload_intrusion/', intrusion.kml_file_upload_intrusion, name="kml_file_upload_intrusion"),
    path('intrusion_kml_edit/<int:id>/', intrusion.intrusion_kml_edit, name="intrusion_kml_edit"),
    path('intrusion_kml_delete/<int:id>/', intrusion.intrusion_kml_delete, name="intrusion_kml_delete"),

    path('boundary_kml_list/', cadastral_entry.boundary_kml_list, name="boundary_kml_list"),
    path('kml_file_upload_boundary/', cadastral_entry.kml_file_upload_boundary, name="kml_file_upload_boundary"),
    path('boundary_kml_edit/<int:id>/', cadastral_entry.boundary_kml_edit, name="boundary_kml_edit"),
    path('boundary_kml_delete/<int:id>/', cadastral_entry.boundary_kml_delete, name="boundary_kml_delete"),


    path('get_settings_ajax/', get_settings_ajax, name="get_settings_ajax"),
    path('', user_login, name="user_login"),
    path('user_menus/', user_menus, name="user_menus"),
    path('settings_screen/', settings_screen, name="settings_screen"),
    path('settings_form/<int:id>', settings_form, name="settings_form"),
    path('user_master_screen/', user_master_screen, name="user_master_screen"),
    path('create_user_master/', create_user_master, name="create_user_master"),
    path('update_user_master/<int:psk_id>/', update_user_master, name="update_user_master"),
    path('delete_user_master/<int:psk_id>/', delete_user_master, name="delete_user_master"),

]
