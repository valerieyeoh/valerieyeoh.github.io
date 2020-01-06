from django.urls import path
from app import views
from django.conf.urls import handler404, handler500
from app.views import error

urlpatterns = [
    path('home', views.home, name='home'),
    path('grains', views.grains, name='grains'),
    path('grains_unit_cost', views.grains_uc, name='grains_uc'),
    path('grains_optimisation', views.grains_opt, name='grains_opt'),
    path('grains_result', views.grains_res, name='grains_res'),
    path('grains_asset', views.grains_asset, name='grains_asset'),
    path('grains_cashflow', views.grains_cashflow, name='grains_cashflow'),
    path('grains_raw_materials', views.grains_raw_materials, name='grains_raw_materials'),
    path('grains_final_products', views.grains_final_products, name='grains_final_products'),
    path('download', views.download, name='download'),
    path('404', views.error, name='error'),
    path('oilseeds', views.oilseeds, name='oilseeds'),
    path('oilseeds_raw_materials', views.oilseeds_raw_materials, name='oilseeds_raw_materials'),
    path('oilseeds_products', views.oilseeds_products, name='oilseeds_products'),
    path('oilseeds_assets', views.oilseeds_assets, name="oilseeds_assets"),
    path('oilseeds_optimisation', views.oilseeds_optimisation, name='oilseeds_optimisation'),
    path('oilseeds_result', views.oilseeds_result, name='oilseeds_result'),
    path('oilseeds_financials', views.oilseeds_financials, name='oilseeds_financials')
]
