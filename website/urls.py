from django.urls import path
from .controllers import auth, dashboard, kelas, siswa, absensi, scanqr, guru, absensiguru

urlpatterns = [
    path('auth/login', auth.views, name='login_views'),
    path('auth/login/authenticate', auth.auth, name='login_auth'),
    path('auth/logout', auth.logouts, name='logout'),

    path('', dashboard.views, name='dashboard_views'),
    path('today', dashboard.get_today, name='dashboard_get_today'),
    path('today-guru', dashboard.get_today_guru, name='dashboard_get_today_guru'),

    path('class', kelas.views, name='class_views'),
    path('class/get-data', kelas.get_data, name='class_get_data'),
    path('class/add', kelas.add_views, name='class_add_views'),
    path('class/add/submit', kelas.add_data, name='class_add_data'),
    path('class/delete', kelas.delete_data, name='class_delete_data'),
    path('class/edit', kelas.edit_data, name='class_edit_data'),
    path('class/upgrade', kelas.upgrade, name='class_upgrade'),

    path('students', siswa.views, name='students_views'),
    path('students/get-data', siswa.get_data, name='students_get_data'),
    path('students/add', siswa.add_views, name='students_add_views'),
    path('students/add/submit', siswa.add_data, name='students_add_data'),
    path('students/delete', siswa.delete_data, name='students_delete_data'),
    path('students/import', siswa.import_file, name='students_import_file'),
    path('students/<int:id>', siswa.edit_views, name='students_edit_views'),
    path('students/<int:id>/get-detail', siswa.get_detail, name='students_edit_get_detail'),
    path('students/<int:id>/submit', siswa.edit_data, name='students_edit_data'),

    path('presences', absensi.views, name='presences_views'),
    path('presences/get-data', absensi.get_data, name='presences_get_data'),
    path('presences/delete', absensi.delete_data, name='presences_delete_data'),
    path('presences/download', absensi.download, name='presences_download_data'),
    path('presences/<int:id>/detail', absensi.detail_views, name='presences_detail_views'),
    path('presences/<int:id>/get-detail', absensi.get_detail, name='presences_get_detail'),

    path('scanqr', scanqr.views, name='scanqr_views'),
    path('scanqr/submit', scanqr.absensi, name='scanqr_absensi'),

    path('teachers', guru.views, name='teachers_views'),
    path('teachers/get-data', guru.get_data, name='teachers_get_data'),
    path('teachers/add', guru.add_views, name='teachers_add_views'),
    path('teachers/add/submit', guru.add_data, name='teachers_add_data'),
    path('teachers/delete', guru.delete_data, name='teachers_delete_data'),
    path('teachers/import', guru.import_file, name='teachers_import_file'),
    path('teachers/<int:id>', guru.edit_views, name='teachers_edit_views'),
    path('teachers/<int:id>/get-detail', guru.get_detail, name='teachers_edit_get_detail'),
    path('teachers/<int:id>/submit', guru.edit_data, name='teachers_edit_data'),

    path('teachers-presences', absensiguru.views, name='teachers_presences_views'),
    path('teachers-presences/get-data', absensiguru.get_data, name='teachers_presences_get_data'),
    path('teachers-presences/delete', absensiguru.delete_data, name='teachers_presences_delete_data'),
    path('teachers-presences/download', absensiguru.download, name='teachers_presences_download_data'),
    path('teachers-presences/<int:id>/detail', absensiguru.detail_views, name='teachers_presences_detail_views'),
    path('teachers-presences/<int:id>/get-detail', absensiguru.get_detail, name='teachers_presences_get_detail'),
]
