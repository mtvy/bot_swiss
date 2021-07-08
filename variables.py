import path

# Last message number
MESSAGE_ID = 42
CHANNEL_ID = -1001216461571

# Id
all_ids_arr = ['281321076', '923118950', '253208582', '169857618', '557561032', '379640085']
label_change_ids_arr  = ['281321076', '923118950']
simple_oper_ids_arr   = ['281321076', '253208582', '923118950', '169857618', '557561032'] 
doctor_oper_ids_arr   = ['281321076', '923118950', '379640085']
support_oper_ids_arr  = ['281321076', '923118950', '379640085']
director_oper_ids_arr = ['281321076', '923118950']
feedback_oper_ids_arr = ['281321076', '923118950', '379640085']
collection_oper_ids_arr = ['281321076']
collection_cash_ids_arr = ['923118950']

# Global variables
account_settings = {}
message_ids_dict = {}
feed_back  = {}
new_acc_id = ""
txt  = ""
mess = ""

# Short operations variables
    # sendReqtoOper
action_oper_select = {
    	'simple_oper' : simple_oper_ids_arr,
    	'doc_oper'    : doctor_oper_ids_arr,
    	'dir_oper'    : director_oper_ids_arr,
    	'sup_oper'    : support_oper_ids_arr
    }

	# selectOffice
show_text_dict = {
    	1 : 'Введите номер терминала:',
    	2 : 'Введите наличные:',
    	3 : 'Ведите номер договора:',
    	4 : 'Введите информацию по возврату средств:',
    	5 : 'Введите данные по ПЦР:',
    	6 : 'Введите данные по ПЦР экспресс:',
    	7 : 'Введите количество анализов:',
    	8 : 'Введите комментарий: ',
    	9 : False
    }

select_collection_action_dict = {
    	0 : 'office',
    	1 : 'terminal_number',
    	2 : 'cash',
    	3 : 'cash_return_info',
    	4 : 'doc_number',
    	5 : 'PCR',
    	6 : 'PCR_express',
    	7 : 'analyzes_count',
    	8 : 'comment',
}

call_data_dict = {
		'Русский'  : ['set_lang', path.first_lang, [["Согласен", "Согласен"], ["Отказываюсь", "Отказываюсь"]]],
    	'Ozbek'    : ['set_lang', path.second_lang, [["ROZIMAN", "Agree"], ["Qo'shilmayman", "Disagree"]]],
		'Отказываюсь' : ['disagree_data', "Вы отказались от обработки персональных данных\n♻️ Для перезапуска бота нажмите /start"],
		'Disagree' : ['disagree_data', "Siz shaxsiy ma'lumotlarni qayta ishlash uchun rad qilgan\n♻️ Botni qayta ishga tushirish uchun bosing /start"],
		'Согласен' : ['agree_data', '♻️ У вас есть реферальная ссылка?', [['Да', 'Да'], ['Нет', 'Нет']]],
		'Agree' : ['agree_data', "♻️ Yo'naltiruvchi havola bormi?", [['Ha', 'Yes'], ["Yo'q", 'No']]],
		'Нет' : ['no_code', 0],
		'No'  : ['no_code', 1],
		'Да'  : ['has_code', '➕ Отправьте код'],
		'Yes'  : ['has_code', '➕ Kodni yuboring'],
		'Написать жалобу' : ['feedback', '➕ Напишите ваше имя', 0],
		'Shikoyat yozing' : ['feedback', '➕ Telefon raqamingizni kiriting', 1],
		'Отправить tag друзей' : ['friends_tag', '➕ Введено 0 из 10 пользователей'],
		'Send friends @tags'   : ['friends_tag', '➕ 10 ta foydalanuvchidan 0 ga kirgan'],
		'Начальный текст' : ['edit_label', [['Русский', 'РусскийLangStart'], ['Ozbek', 'OzbekLangStart']]],
		'FAQ текст' : ['edit_label', [['Русский', 'РусскийLangFAQ'], ['Ozbek', 'OzbekLangFAQ']]],
		'Текст оператора': ['edit_label', [['Русский', 'РусскийLangOper'], ['Ozbek', 'OzbekLangOper']]],
		'Текст телефона' : ['edit_label', [['Русский', 'РусскийLangTele'], ['Ozbek', 'OzbekLangTele']]],
		'Текст адресса': ['edit_label', [['Русский', 'РусскийLangAdress'], ['Ozbek', 'OzbekLangAdress']]],
		'Текст создания заказа': ['edit_label', [['Русский', 'РусскийLangOrder'], ['Ozbek', 'OzbekLangOrder']]],
		'Текст отзыва': ['edit_label', [['Русский', 'РусскийLangRecv'], ['Ozbek', 'OzbekLangRecv']]],
		'Текст скидки': ['edit_label', [['Русский', 'РусскийLangDisc'], ['Ozbek', 'OzbekLangDisc']]],
		'Текст социальные сети': ['edit_label', [['Русский', 'РусскийLangSocial'], ['Ozbek', 'OzbekLangSocial']]],
		'Текст инструкции оператора': ['edit_label', [['Русский', 'РусскийLangOperFAQ'], ['Ozbek', 'OzbekLangOperFAQ']]],
		'РусскийLangStart': ['edit_label_sec', path.first_lang],
		'OzbekLangStart': ['edit_label_sec', path.second_lang],
		'РусскийLangFAQ': ['edit_label_sec', path.FAQ_label],
		'OzbekLangFAQ': ['edit_label_sec', path.sec_FAQ_label],
		'РусскийLangOper': ['edit_label_sec', path.oper_label],
		'OzbekLangOper': ['edit_label_sec', path.sec_oper_label],
		'РусскийLangTele': ['edit_label_sec', path.telephone_num],
		'OzbekLangTele': ['edit_label_sec', path.sec_telephone_num],
		'РусскийLangAdress': ['edit_label_sec', path.address_label],
		'OzbekLangAdress': ['edit_label_sec', path.sec_address_label],
		'РусскийLangOrder': ['edit_label_sec', path.order_label],
		'OzbekLangOrder': ['edit_label_sec', path.sec_order_label],
		'РусскийLangRecv': ['edit_label_sec', path.recv_label],
		'OzbekLangRecv': ['edit_label_sec', path.sec_recv_label],
		'РусскийLangDisc': ['edit_label_sec', path.discount_label],
		'OzbekLangDisc': ['edit_label_sec', path.sec_discount_label],
		'РусскийLangSocial': ['edit_label_sec', path.social_web],
		'OzbekLangSocial': ['edit_label_sec', path.sec_social_web],
		'РусскийLangOperFAQ': ['edit_label_sec', path.FAQoper_label],
		'OzbekLangOperFAQ': ['edit_label_sec', path.sec_FAQoper_label],
		'Номер терминала' : ['office_edit', 1],
    	'Исправить наличные' : ['office_edit', 2],
    	'Информация по возврату средств' : ['office_edit', 3],
    	'Номер договора' : ['office_edit', 4],
    	'Данные по ПЦР' : ['office_edit', 5],
    	'Данные по ПЦР экспресс' : ['office_edit', 6],
    	'Количество анализов' : ['office_edit', 7],
    	'Комментарий' : ['office_edit', 8]
}

buttons_ru_text = {
		'📞 Телефон' : ['oper', 'user', 'admin'],
		'🏠 Адреса' : ['oper', 'user', 'admin'],
		'🙋 Оператор' : ['user'],
		'📝 Создать заказ' : ['oper', 'user', 'admin'],
		'❗️ Оставить жалобу' : ['oper', 'user', 'admin'],
		'💽 БД переписок' : ['oper', 'admin'],
		'% Получить скидку' : ['oper', 'user', 'admin'],
		'®FAQ Инструкция' : ['oper', 'user', 'admin'],
		'✍️ Написать директору' : ['user'],
		'🌐 Соц. сети' : ['oper', 'user', 'admin'],
		'☎️ Тех. поддержка' : ['user'],
		'👨‍⚕️ Доктор онлайн' : ['user'],
		'💰 Инкассация' : ['admin']
	}

buttons_uz_text = {
		'📞 telefon' : ['oper', 'user', 'admin'],
		'🏠 manzillari' : ['oper', 'user', 'admin'],
		'🙋 Operator' : ['user'],
		'📝 buyurtma yaratish' : ['oper', 'user', 'admin'],
		'❗️ Shikoyat qoldiring' : ['oper', 'user', 'admin'],
		'💽 Yozishmalar bazasi' : ['oper', 'admin'],
		'% Chegirma oling' : ['oper', 'user', 'admin'],
		"®FAQ Ko'rsatma" : ['oper', 'user', 'admin'],
		'✍️ Direktorga yozing' : ['user'],
		'🌐 Biz ijtimoiy tarmoqlarda' : ['oper', 'user', 'admin'],
		"☎️ O'sha.  qo'llab-quvvatlash" : ['user'],
		'👨‍⚕️ Shifokor onlayn' : ['user'],
		"💰 Naqd pul yig'ish" : ['admin']
	}

buttons_oper_text = {
		'🔙 Отклонить вызов оператора' : ['redirect', 'person'],
		'❔ Инструкция' : ['redirect', 'person'],
		'❗️ Жалоба' : ['redirect'],
		'🙋 Операторская' : ['redirect'],
		'☎️ Поддержка' : ['redirect'],
		'✍️ Директор' : ['redirect'],
		'👨‍⚕️ Доктор' : ['redirect']
	}

buttons_user_uz_text = {
	"🔙 Operator chaqiruvini rad etish" :['person'],
	"❔ Ko'rsatma" : ['person']
}

	# main def message.text variables
message_text_dict = {
    	'МО Гор.больница №1' : ['office'],
    	'МО Кушбеги'         : ['office'],
    	'МО  Мирзо Улугбека' : ['office'],
    	'МО  Юнусата'        : ['office'],     
    	'МО  viezd'          : ['office'],
		'❔ Инструкция' : ['text_show', path.FAQoper_label, path.sec_FAQoper_label],
		"❔ Ko'rsatma"  : ['text_show', path.FAQoper_label, path.sec_FAQoper_label],
    	'📞 Телефон'    : ['text_show', path.telephone_num, path.sec_telephone_num],
    	'📞 telefon'    : ['text_show', path.telephone_num, path.sec_telephone_num],
    	'🏠 Адреса'     : ['text_show', path.address_label, path.sec_address_label],
    	'🏠 manzillari' : ['text_show', path.address_label, path.sec_address_label],
    	'🌐 Соц. сети'  : ['text_show', path.social_web, path.sec_social_web],
    	'🌐 Biz ijtimoiy tarmoqlarda' : ['text_show', path.social_web, path.sec_social_web],
    	'®FAQ Инструкция'  : ['text_show', path.FAQ_label, path.sec_FAQ_label],
    	"®FAQ Ko'rsatma"   : ['text_show', path.FAQ_label, path.sec_FAQ_label],
    	'📝 Создать заказ'     : ['text_show', path.order_label, path.sec_order_label],
    	'📝 buyurtma yaratish' : ['text_show', path.order_label, path.sec_order_label],
    	'🙋 Оператор'        : ['oper_show', simple_oper_ids_arr, 'simple_oper'],
    	'🙋 Operator'        : ['oper_show', simple_oper_ids_arr, 'simple_oper'],
    	'👨‍⚕️ Доктор онлайн'   : ['oper_show', doctor_oper_ids_arr, 'doc_oper'],
    	'👨‍⚕️ Shifokor onlayn' : ['oper_show', doctor_oper_ids_arr, 'doc_oper'],
    	'☎️ Тех. поддержка'  : ['oper_show', support_oper_ids_arr, 'sup_oper'],
    	'☎️ Тех. поддержка'  : ['oper_show', support_oper_ids_arr, 'sup_oper'],
    	'✍️ Написать директору' : ['oper_show', director_oper_ids_arr, 'dir_oper'],
    	'✍️ Direktorga yozing'  : ['oper_show', director_oper_ids_arr, 'dir_oper'],
    	'🔙 Отклонить вызов оператора'      : ['oper_close', 0],
    	'🔙 Operator chaqiruvini rad etish' : ['oper_close', 1],
    	'🙋 Операторская' : ['redirect', 'к оператору', simple_oper_ids_arr, 'simple_oper'],
    	'☎️ Поддержка'    : ['redirect', 'в тех.поддержку', support_oper_ids_arr, 'sup_oper'],
    	'✍️ Директор'     : ['redirect', 'к директору', director_oper_ids_arr, 'dir_oper' ],
    	'👨‍⚕️ Доктор'       : ['redirect', 'к доктору', doctor_oper_ids_arr, 'doc_oper']
}

markup_change_label_arr = [
		["FAQ текст", "FAQ текст"], 
		["Текст отзыва", "Текст отзыва"], 
		["Текст скидки", "Текст скидки"],
		["Текст адресса", "Текст адресса"], 
		["Текст телефона", "Текст телефона"], 
        ["Начальный текст", "Начальный текст"], 
		["Текст оператора", "Текст оператора"],
		["Текст создания заказа", "Текст создания заказа"], 
        ["Текст социальные сети", "Текст социальные сети"], 
		["Текст инструкции оператора", "Текст инструкции оператора"]
]

markup_change_collection_arr = [
	['Комментарий', 'Комментарий'],
	['Данные по ПЦР', 'Данные по ПЦР'],
	['Номер договора', 'Номер договора'],
	['Номер терминала', 'Номер терминала'],
	['Исправить наличные', 'Исправить наличные'],
	['Количество анализов', 'Количество анализов'],
	['Данные по ПЦР экспресс', 'Данные по ПЦР экспресс'],
	['Информация по возврату средств', 'Информация по возврату средств'],
]

office_markup_dict = {
	"МО Гор.больница №1" : ['office'],
	"МО Кушбеги" : ['office'],
	"МО  Мирзо Улугбека" : ['office'],
	"МО  Юнусата" : ['office'],
	"МО  viezd" : ['office'],
	"🔙 Назад" : ['office']
}