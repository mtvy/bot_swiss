import path

# Last message number
MESSAGE_ID = 254

# Id
all_ids_arr = ['281321076', '923118950', '169857618', '805485641', '557561032', '379640085']
label_change_ids_arr  = ['281321076', '923118950']
simple_oper_ids_arr   = ['281321076', '923118950', '169857618', '805485641', '557561032'] 
doctor_oper_ids_arr   = ['281321076', '923118950', '379640085']
support_oper_ids_arr  = ['281321076', '923118950', '379640085']
director_oper_ids_arr = ['281321076', '923118950']
feedback_oper_ids_arr = ['281321076', '923118950', '379640085']
collection_oper_ids_arr = ['281321076']
collection_cash_ids_arr = ['']

# Global variables
account_settings = {}
message_ids_dict = {}
feed_back  = {}
new_acc_id = ""
txt  = ""
mess = ""

# Short operations variables
	# checkOperId
action_dict = {
    	'check_all_oper'   : all_ids_arr,
    	'check_simple_oper': simple_oper_ids_arr,
    	'check_doc_id'     : doctor_oper_ids_arr,
    	'check_support_id' : support_oper_ids_arr,
    	'check_feedback_oper_id' : feedback_oper_ids_arr,
    	'check_director_id'      : director_oper_ids_arr,
    	'check_label_changer'    : label_change_ids_arr,
    	'check_collection_oper'  : collection_oper_ids_arr,
		'check_collection_cash'  : collection_cash_ids_arr
    }
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

call_data_office_dict = {
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
			'✍️ Написать директору' : ['user']
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
			'✍️ Direktorga yozing' : ['user']
			'🌐 Biz ijtimoiy tarmoqlarda' : ['oper', 'user', 'admin'],
			"☎️ O'sha.  qo'llab-quvvatlash" : ['user'],
			'👨‍⚕️ Shifokor onlayn' : ['user'],
			"💰 Naqd pul yig'ish" : ['admin']
	}

	# main def message.text variables
message_text_dict = {
    	'МО Гор.больница №1' : ['office'],
    	'МО Кушбеги'         : ['office'],
    	'МО  Мирзо Улугбека' : ['office'],
    	'МО  Юнусата'        : ['office'],     
    	'МО  viezd'          : ['office'],
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
    	'% Получить скидку'     : ['discount', path.discount_label],
    	'% Chegirma oling'      : ['discount', path.sec_discount_label],
    	'🙋 Оператор'        : ['oper_show', 'check_simple_oper', 'simple_oper'],
    	'🙋 Operator'        : ['oper_show', 'check_simple_oper', 'simple_oper'],
    	'👨‍⚕️ Доктор онлайн'   : ['oper_show', 'check_doc_id', 'doc_oper'],
    	'👨‍⚕️ Shifokor onlayn' : ['oper_show', 'check_doc_id', 'doc_oper'],
    	'☎️ Тех. поддержка'  : ['oper_show', 'check_support_id', 'sup_oper'],
    	'☎️ Тех. поддержка'  : ['oper_show', 'check_support_id', 'sup_oper'],
    	'✍️ Написать директору' : ['oper_show', 'check_director_id', 'dir_oper'],
    	'✍️ Direktorga yozing'  : ['oper_show', 'check_director_id', 'dir_oper'],
    	'❗️ Оставить жалобу'    : [''],
    	'❗️ Shikoyat qoldiring' : [''],
    	'💰 Инкассация'         : [''],
    	'💽 БД переписок'       : [''],
    	'💽 Yozishmalar bazasi' : [''],
    	'🔙 Отклонить вызов оператора'      : ['oper_close', 0],
    	'🔙 Operator chaqiruvini rad etish' : ['oper_close', 1],
    	'❗️ Жалоба'         : [''],
    	'❗️ Жалоба'         : [''],
    	'🙋 Операторская' : ['redirect', 'к оператору', 'check_simple_oper', 'simple_oper'],
    	'☎️ Поддержка'    : ['redirect', 'в тех.поддержку', 'check_support_id', 'sup_oper'],
    	'✍️ Директор'     : ['redirect', 'к директору', 'check_director_id', 'dir_oper' ],
    	'👨‍⚕️ Доктор'       : ['redirect', 'к доктору', 'check_doc_id', 'doc_oper'],
    	'❔ Инструкция'   : [''],
    	"❔ Ko'rsatma"    : [''],
    	''         : [''],
    	''         : [''],
    	''         : [''],
    	''         : ['']
    }

