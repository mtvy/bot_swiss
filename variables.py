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
    	'check_collection_oper'  : collection_oper_ids_arr
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

	# main def message.text variables
message_text_dict = {
    	'МО Гор.больница №1' : ['office'],
    	'МО Кушбеги'         : ['office'],
    	'МО  Мирзо Улугбека' : ['office'],
    	'МО  Юнусата'        : ['office'],     
    	'МО  viezd'          : ['office'],
    	'📞 Телефон'    : ['text_show', path_telephone_num, path_sec_telephone_num],
    	'📞 telefon'    : ['text_show', path_telephone_num, path_sec_telephone_num],
    	'🏠 Адреса'     : ['text_show', path_address_label, path_sec_address_label],
    	'🏠 manzillari' : ['text_show', path_address_label, path_sec_address_label],
    	'🌐 Соц. сети'  : ['text_show', path_social_web, path_sec_social_web],
    	'🌐 Biz ijtimoiy tarmoqlarda' : ['text_show', path_social_web, path_sec_social_web],
    	'®FAQ Инструкция'  : ['text_show', path_FAQ_label, path_sec_FAQ_label],
    	"®FAQ Ko'rsatma"   : ['text_show', path_FAQ_label, path_sec_FAQ_label],
    	'📝 Создать заказ'     : ['text_show', path_order_label, path_sec_order_label],
    	'📝 buyurtma yaratish' : ['text_show', path_order_label, path_sec_order_label],
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
    	'% Получить скидку'     : ['discount', 'path_FAQoper_label'],
    	'% Chegirma oling'      : ['discount', 'path_sec_FAQoper_label'],
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

