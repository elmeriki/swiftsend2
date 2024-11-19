
from django.urls import path,include
from customer import views

urlpatterns = [
    path('add', views.add_customerView, name='add_customerView'),
    path('register', views.register_customerView, name='register_customerView'),
    path('user_info/<int:user_id>', views.user_infoView, name='user_infoView'),
    path('send_sms', views.send_smsView, name='send_smsView'),
    path('send_email', views.send_emailView, name='send_emailView'),
    path('users', views.usersView, name='usersView'),
    path('import_leads', views.import_leadsView, name='import_leadsView'),
    path('update_user/<int:user_id>', views.update_userView, name='update_userView'),
    path('update_users/<int:user_id>', views.update_usersView, name='update_usersView'),
    
    path('birthday', views.birthdayView, name='birthdayView'),
    path('reminder', views.reminderView, name='reminderView'),
    path('delete_user/<int:user_id>', views.delete_userView, name='delete_userView'),
    path('search_user', views.search_userView, name='search_userView'),
    path('message', views.messageView, name='messageView'),
    path('import_lead_', views.import_leadView, name='import_leadView'),
    
    
    path('schedule_send_sms', views.schedule_send_smsView, name='schedule_send_smsView'),
    path('schedule__send_email', views.schedule_send_emailView, name='schedule_send_emailView'),
    
    path('sms_log', views.sms_logView, name='sms_logView'),
    path('email_log', views.email_logView, name='email_logView'),

    path('my_log', views.my_logView, name='my_logView'),
    path('my_log_completed/<int:id>', views.my_log_completedView, name='my_log_completedView'),
    path('my_log_unmark/<int:id>', views.my_log_unmarkView, name='my_log_unmarkView'),
    path('delete_log/<int:id>', views.delete_logView, name='delete_logView'),
    
    path('template_galery', views.template_galeryView, name='template_galeryView'),
    path('template1', views.template1View, name='template1View'),
    path('template2', views.template2View, name='template2View'),
    path('template3', views.template3View, name='template3View'),
    path('template4', views.template4View, name='template4View'),
    
    path('preview_draft_template/<int:id>', views.preview_draft_template, name='preview_draft_template'),

    path('update_template_1/<int:id>', views.update_template_1, name='update_template_1'),
    path('update_template_1_/<int:id>', views.update_template_1_, name='update_template_1_'),

    path('customise_template_2', views.customise_template_2View, name='customise_template_2View'),
    path('create_template2', views.create_template2View, name='create_template2View'),
    path('template2_draft', views.template2_draftView, name='template2_draftView'),
    path('preview_draft_template2/<int:id>', views.preview_draft_template2, name='preview_draft_template2'),
    path('update_template_2/<int:id>', views.update_template_2, name='update_template_2'),
    path('update_template_2_/<int:id>', views.update_template_2_, name='update_template_2_'),
    path('delete_template2/<int:id>', views.delete_template2View, name='delete_template2View'),
    path('list_template2/<int:id>', views.add_list_template2, name='add_list_template2'),
    path('save_list_template2/<int:id>', views.save_list_template2View, name='save_list_template2View'),
    path('delete_template2_list/<int:id>', views.delete_template2_listView, name='delete_template2_listView'),
    
    
    path('customise_template_3', views.customise_template_3View, name='customise_template_3View'),
    path('create_template3', views.create_template3View, name='create_template3View'),
    path('template3_draft', views.template3_draftView, name='template3_draftView'),
    path('preview_draft_template3/<int:id>', views.preview_draft_template3, name='preview_draft_template3'),
    path('update_template_3/<int:id>', views.update_template_3, name='update_template_3'),
    path('update_template_3_/<int:id>', views.update_template_3_, name='update_template_3_'),
    path('delete_template3/<int:id>', views.delete_template3View, name='delete_template3View'),


    path('customise_template_4', views.customise_template_4View, name='customise_template_4View'),
    path('create_template4', views.create_template4View, name='create_template4View'),
    path('template4_draft', views.template4_draftView, name='template4_draftView'),
    path('preview_draft_template4/<int:id>', views.preview_draft_template4, name='preview_draft_template4'),
    path('update_template_4/<int:id>', views.update_template_4, name='update_template_4'),
    path('update_template_4_/<int:id>', views.update_template_4_, name='update_template_4_'),
    path('delete_template4/<int:id>', views.delete_template4View, name='delete_template4View'),
    path('paragraph_template4/<int:id>', views.paragraph_template4, name='paragraph_template4'),
    path('save_paragraph_template4/<int:id>', views.save_paragraph_template4, name='save_paragraph_template4'),
    path('delete_template4_paragraph/<int:id>', views.delete_template4_paragraphView, name='delete_template4_paragraphView'),


    path('customise_template_1', views.customise_template_1View, name='customise_template_1View'),
    path('template1_draft', views.template1_draftView, name='template1_draftView'),
    path('create_template1', views.create_template1View, name='create_template1View'),

    path('delete_template1/<int:id>', views.delete_template1View, name='delete_template1View'),
    path('product_template1/<int:id>', views.add_product_template1View, name='add_product_template1View'),
    
    path('save_product_template1/<int:id>', views.save_product_template1View, name='save_product_template1View'),
    path('delete_template1_product/<int:id>', views.delete_template1_productView, name='delete_template1_productView'),

]
