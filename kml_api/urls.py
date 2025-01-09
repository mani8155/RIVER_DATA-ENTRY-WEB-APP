from django.urls import path
from . import views


urlpatterns = [
   path('list_type_api/', views.list_types, name="list-type-api"),
   path('list_of_values_list/', views.list_of_values_list, name="list_of_values_list"),
   path('street_lists/', views.street_lists, name="street_lists"),
   path('cadastral_line_lists/', views.cadastral_line_lists, name="cadastral_line_lists"),
   path('boundary_pillar_lists/', views.boundary_pillar_lists, name="boundary_pillar_lists"),
   path('enchrochments_lists/', views.enchrochments_lists, name="enchrochments_lists"),
   path('intrusion_lists/', views.intrusion_lists, name="intrusion_lists"),


   path('list_type_excel/', views.list_type_excel, name="list_type_excel"),
   path('street_excel_import/', views.street_excel_import, name="street_excel_import"),
   path('cm_excel_import/', views.CM_excel_import, name="cm_excel_import"),
   path('boundarypillar_excel_import/', views.boundaryPillar_excel_import, name="boundarypillar_excel_import"),
   path('cd_excel_import/', views.CD_excel_import, name="cd_excel_import"),
   path('intrusion_excel_import/', views.intrusion_excel_import, name="intrusion_excel_import"),

   path('cadastral_master_kml/<str:river_name>/', views.cadastral_master_kml, name="cadastral_master_kml"),
   path('boundary_pillar_kml/<str:river_name>/', views.boundary_pillar_kml, name="boundary_pillar_kml"),
   path('enchrochment_kml/<str:river_name>/', views.enchrochment_kml, name="enchrochment_kml"),
   path('intrusion_kml/<str:river_name>/', views.intrusion_kml, name="intrusion_kml"),

   path('cl_river_list/', views.CL_river_list, name="cl_river_list"),
   path('boundary_river_list/', views.boundary_river_list, name="boundary_river_list"),
   path('enchrochment_river_list/', views.enchrochment_river_list, name="enchrochment_river_list"),
   path('intrusion_river_list/', views.intrusion_river_list, name="intrusion_river_list"),

   path('boundary_pillar_photos/<str:unique_id>/', views.boundary_pillar_photos, name="boundary_pillar_photos"),

]
