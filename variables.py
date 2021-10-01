import path
import emj

CHANNEL_ID = -1001216461571

# Id
all_ids_arr              =  [ '281321076'  , '923118950'  , '253208582'  ]
simple_oper_ids_arr      =  [ '281321076'  , '923118950'  , '253208582'  ] 
doctor_oper_ids_arr      =  [ '281321076'  , '923118950'  , '253208582'  ]
label_change_ids_arr     =  [ '281321076'  , '923118950'                 ]
support_oper_ids_arr     =  [ '281321076'  , '923118950'  , '253208582'  ]
director_oper_ids_arr    =  [ '281321076'  , '923118950'  , '253208582'  ]
feedback_oper_ids_arr    =  [ '281321076'  , '923118950'  , '253208582'  ]
collection_oper_ids_arr  =  [ '923118950'  , '1670603092' , '1704859354' ,
                              '1778013650' , '1788724487' , '1527064392' ]
collection_cash_ids_arr  =  [ '281321076'  , '992113168'  ]
 

# Global variables
account_settings    =  {}
message_ids_dict    =  {}
feed_back           =  {}
new_acc_id          =  ""
txt                 =  ""
mess                =  ""


# Short operations variables

    # sendReqtoOper
action_oper_select = {
	'simple_oper' : simple_oper_ids_arr  ,
	'doc_oper'    : doctor_oper_ids_arr  ,
	'dir_oper'    : director_oper_ids_arr,
	'sup_oper'    : support_oper_ids_arr
}


	# selectOffice
add_text_dict = [
	'ID записи:'                     ,
	'ID админа:'                     ,
	'ID кассира:'                    ,
	'Офис:'                          ,
	'Номер терминала:'               ,
	'Наличные:'                      ,
	'Номер договора:'                ,
	'Информацию по возврату средств:',
	'Данные по ПЦР:'                 ,
	'Данные по ПЦР экспресс:'        ,
	'Количество анализов:'           ,
	'Комментарий:'
]

show_text_dict = {
	1 : 'Введите номер терминала:'               ,
	2 : 'Введите наличные:'                      ,
	3 : 'Ведите номер договора:'                 ,
	4 : 'Введите информацию по возврату средств:',
	5 : 'Введите данные по ПЦР:'                 ,
	6 : 'Введите данные по ПЦР экспресс:'        ,
	7 : 'Введите количество анализов:'           ,
	8 : 'Введите комментарий: '                  ,
	9 : False
}

select_collection_action_dict = {
	0 : 'office'           ,
	1 : 'terminal_number'  ,
	2 : 'cash'             ,
	3 : 'cash_return_info' ,
	4 : 'doc_number'       ,
	5 : 'PCR'              ,
	6 : 'PCR_express'      ,
	7 : 'analyzes_count'   ,
	8 : 'comment'
}

call_data_dict = {
	'Русский'                       : ['set_lang'      , path.first_lang , [["Согласен", "Согласен"], ["Отказываюсь"  , "Отказываюсь"]]         ],
	'Ozbek'                         : ['set_lang'      , path.second_lang, [["ROZIMAN" , "Agree"   ], ["Qo'shilmayman", "Disagree"   ]]         ],
	'Отказываюсь'                   : ['disagree_data' , "Вы отказались от обработки персональных данных\n Для перезапуска бота нажмите /start" ],
	'Disagree'                      : ['disagree_data' , f"Siz shaxsiy ma'lumotlarni qayta ishlash uchun rad qilgan\n"
                                                         f"{emj.EMJ_RECYCLING} Botni qayta ishga tushirish uchun bosing /start"                 ],
	'Согласен'                      : ['agree_data'    , f'{emj.EMJ_RECYCLING} У вас есть реферальная ссылка?', [['Да', 'Да' ], ['Нет' , 'Нет']]],
	'Agree'                         : ['agree_data'    , f"{emj.EMJ_RECYCLING} Yo'naltiruvchi havola bormi?"  , [['Ha', 'Yes'], ["Yo'q", 'No' ]]],
	'Нет'                           : ['no_code'       , 0                                                                     ],
	'No'                            : ['no_code'       , 1                                                                     ],
	'Да'                            : ['has_code'      , f'{emj.EMJ_PLUS} Отправьте код'                                       ],
	'Yes'                           : ['has_code'      , f'{emj.EMJ_PLUS} Kodni yuboring'                                      ],
	'Написать жалобу'               : ['feedback'      , f'{emj.EMJ_PLUS} Напишите ваше имя'             , 0                   ],
	'Shikoyat yozing'               : ['feedback'      , f'{emj.EMJ_PLUS} Telefon raqamingizni kiriting' , 1                   ],
	'Отправить tag друзей'          : ['friends_tag'   , f'{emj.EMJ_PLUS} Введено 0 из 10 пользователей'                       ],
	'Send friends @tags'            : ['friends_tag'   , f'{emj.EMJ_PLUS} 10 ta foydalanuvchidan 0 ga kirgan'                  ],
	'Начальный текст'               : ['edit_label'    , [['Русский', 'РусскийLangStart'  ],     ['Ozbek', 'OzbekLangStart'  ]]],
	'FAQ текст'                     : ['edit_label'    , [['Русский', 'РусскийLangFAQ'    ],     ['Ozbek', 'OzbekLangFAQ'    ]]],
	'Текст оператора'               : ['edit_label'    , [['Русский', 'РусскийLangOper'   ],     ['Ozbek', 'OzbekLangOper'   ]]],
	'Текст телефона'                : ['edit_label'    , [['Русский', 'РусскийLangTele'   ],     ['Ozbek', 'OzbekLangTele'   ]]],
	'Текст адресса'                 : ['edit_label'    , [['Русский', 'РусскийLangAdress' ],     ['Ozbek', 'OzbekLangAdress' ]]],
	'Текст создания заказа'         : ['edit_label'    , [['Русский', 'РусскийLangOrder'  ],     ['Ozbek', 'OzbekLangOrder'  ]]],
	'Текст отзыва'                  : ['edit_label'    , [['Русский', 'РусскийLangRecv'   ],     ['Ozbek', 'OzbekLangRecv'   ]]],
	'Текст скидки'                  : ['edit_label'    , [['Русский', 'РусскийLangDisc'   ],     ['Ozbek', 'OzbekLangDisc'   ]]],
	'Текст социальные сети'         : ['edit_label'	   , [['Русский', 'РусскийLangSocial' ],     ['Ozbek', 'OzbekLangSocial' ]]],
	'Текст инструкции оператора'    : ['edit_label'	   , [['Русский', 'РусскийLangOperFAQ'],     ['Ozbek', 'OzbekLangOperFAQ']]],
	'РусскийLangStart'              : ['edit_label_sec', path.first_lang                  ],
	'OzbekLangStart'                : ['edit_label_sec', path.second_lang                 ],
	'РусскийLangFAQ'                : ['edit_label_sec', path.FAQ_label                   ],
	'OzbekLangFAQ'                  : ['edit_label_sec', path.sec_FAQ_label               ],
	'РусскийLangOper'               : ['edit_label_sec', path.oper_label                  ],
	'OzbekLangOper'                 : ['edit_label_sec', path.sec_oper_label              ],
	'РусскийLangTele'               : ['edit_label_sec', path.telephone_num               ],
	'OzbekLangTele'                 : ['edit_label_sec', path.sec_telephone_num           ],
	'РусскийLangAdress'             : ['edit_label_sec', path.address_label               ],
	'OzbekLangAdress'               : ['edit_label_sec', path.sec_address_label           ],
	'РусскийLangOrder'              : ['edit_label_sec', path.order_label                 ],
	'OzbekLangOrder'                : ['edit_label_sec', path.sec_order_label             ],
	'РусскийLangRecv'               : ['edit_label_sec', path.recv_label                  ],
	'OzbekLangRecv'                 : ['edit_label_sec', path.sec_recv_label              ],
	'РусскийLangDisc'               : ['edit_label_sec', path.discount_label              ],
	'OzbekLangDisc'                 : ['edit_label_sec', path.sec_discount_label          ],
	'РусскийLangSocial'             : ['edit_label_sec', path.social_web                  ],
	'OzbekLangSocial'               : ['edit_label_sec', path.sec_social_web              ],
	'РусскийLangOperFAQ'            : ['edit_label_sec', path.FAQoper_label               ],
	'OzbekLangOperFAQ'              : ['edit_label_sec', path.sec_FAQoper_label           ],
	'Номер терминала'               : ['office_edit'   , 1                                ],
	'Исправить наличные'            : ['office_edit'   , 2                                ],
	'Информация по возврату средств': ['office_edit'   , 3                                ],
	'Номер договора'                : ['office_edit'   , 4                                ],
	'Данные по ПЦР'                 : ['office_edit'   , 5                                ],
	'Данные по ПЦР экспресс'        : ['office_edit'   , 6                                ],
	'Количество анализов'           : ['office_edit'   , 7                                ],
	'Комментарий'                   : ['office_edit'   , 8                                ]
}

buttons_ru_text = {
	f'{emj.EMJ_TELEPHONE} Телефон'                          : ['oper' , 'user' , 'admin'],
	f'{emj.EMJ_HOUSE} Адреса'                               : ['oper' , 'user' , 'admin'],
	f'{emj.EMJ_RAISING_HAND} Оператор'                      : ['user'                   ],
	f'{emj.EMJ_NOTE} Создать заказ'                         : ['user'                   ],
	f'{emj.EMJ_BACK_ARROW} Отклонить вызов оператора'       : ['oper' , 'admin'         ],
	f'{emj.EMJ_EXCLAMATION} Оставить жалобу'                : ['oper' , 'user' , 'admin'],
	f'{emj.EMJ_DISK} БД переписок'                          : ['oper' , 'admin'         ],
	'% Получить скидку'                                     : ['oper' , 'user' , 'admin'],
	f'{emj.EMJ_INFO} FAQ Инструкция'                        : ['oper' , 'user' , 'admin'],
	f'{emj.EMJ_WRITING_HAND} Написать директору'            : ['user'                   ],
	f'{emj.EMJ_GLOBE} Соц. сети'                            : ['oper' , 'user' , 'admin'],
	f'{emj.EMJ_OLD_TELEPHONE} Тех. поддержка'               : ['user'                   ],
	f'{emj.EMJ_DOCTOR} Доктор онлайн'                       : ['user'                   ],
	f'{emj.EMJ_MONEY_BAG} Инкассация'                       : ['admin'                  ]
}

buttons_uz_text = {
	f'{emj.EMJ_TELEPHONE} telefon'                          : ['oper', 'user', 'admin'],
	f'{emj.EMJ_HOUSE} manzillari'                           : ['oper', 'user', 'admin'],
	f'{emj.EMJ_RAISING_HAND} Operator'                      : ['user'                 ],
	f'{emj.EMJ_NOTE} buyurtma yaratish'                     : ['user'                 ],
	f'{emj.EMJ_BACK_ARROW} Operator chaqiruvini rad etish'  : ['oper', 'admin'        ],
	f'{emj.EMJ_EXCLAMATION} Shikoyat qoldiring'             : ['oper', 'user', 'admin'],
	f'{emj.EMJ_DISK} Yozishmalar bazasi'                    : ['oper', 'admin'        ],
	'% Chegirma oling'                                      : ['oper', 'user', 'admin'],
	f"{emj.EMJ_INFO} FAQ Ko'rsatma"                         : ['oper', 'user', 'admin'],
	f'{emj.EMJ_WRITING_HAND} Direktorga yozing'             : ['user'                 ],
	f'{emj.EMJ_GLOBE} Biz ijtimoiy tarmoqlarda'             : ['oper', 'user', 'admin'],
	f"{emj.EMJ_OLD_TELEPHONE} O'sha.  qo'llab-quvvatlash"   : ['user'                 ],
	f'{emj.EMJ_DOCTOR} Shifokor onlayn'                     : ['user'                 ],
	f"{emj.EMJ_MONEY_BAG} Naqd pul yig'ish"                 : ['admin'                ]
}

buttons_oper_text = {
	f'{emj.EMJ_BACK_ARROW} Отклонить вызов оператора'       : ['redirect', 'person'],
	f'{emj.EMJ_QUESTION} Инструкция'                        : ['redirect', 'person'],
	f'{emj.EMJ_EXCLAMATION} Жалоба'                         : ['redirect'          ],
	f'{emj.EMJ_RAISING_HAND} Операторская'                  : ['redirect'          ],
	f'{emj.EMJ_OLD_TELEPHONE} Поддержка'                    : ['redirect'          ],
	f'{emj.EMJ_WRITING_HAND} Директор'                      : ['redirect'          ],
	f'{emj.EMJ_DOCTOR} Доктор'                              : ['redirect'          ]
}

buttons_user_uz_text = {
	f"{emj.EMJ_BACK_ARROW} Operator chaqiruvini rad etish"  : ['person'],
	f"{emj.EMJ_QUESTION} Ko'rsatma"                         : ['person']
}


	# main def message.text variables
message_text_dict = {
	'МО Гор.больница №1'                                    : ['office'   ],
	'МО Кушбеги'                                            : ['office'   ],
	'МО  Мирзо Улугбека'                                    : ['office'   ],
	'МО  Юнусата'                                           : ['office'   ],
	'МО  viezd'                                             : ['office'   ],
	f'{emj.EMJ_QUESTION} Инструкция'                        : ['text_show' , path.FAQoper_label   , path.sec_FAQoper_label],
	f"{emj.EMJ_QUESTION} Ko'rsatma"                         : ['text_show' , path.FAQoper_label   , path.sec_FAQoper_label],
	f'{emj.EMJ_TELEPHONE} Телефон'                          : ['text_show' , path.telephone_num   , path.sec_telephone_num],
	f'{emj.EMJ_TELEPHONE} telefon'                          : ['text_show' , path.telephone_num   , path.sec_telephone_num],
	f'{emj.EMJ_HOUSE} Адреса'                               : ['text_show' , path.address_label   , path.sec_address_label],
	f'{emj.EMJ_HOUSE} manzillari'                           : ['text_show' , path.address_label   , path.sec_address_label],
	f'{emj.EMJ_GLOBE} Соц. сети'                            : ['text_show' , path.social_web      , path.sec_social_web	  ],
	f'{emj.EMJ_GLOBE} Biz ijtimoiy tarmoqlarda'             : ['text_show' , path.social_web      , path.sec_social_web   ],
	f'{emj.EMJ_INFO} FAQ Инструкция'                        : ['text_show' , path.FAQ_label       , path.sec_FAQ_label    ],
	f"{emj.EMJ_INFO} FAQ Ko'rsatma"                         : ['text_show' , path.FAQ_label       , path.sec_FAQ_label    ],
	f'{emj.EMJ_NOTE} Создать заказ'                         : ['text_show' , path.order_label     , path.sec_order_label  ],
	f'{emj.EMJ_NOTE} buyurtma yaratish'                     : ['text_show' , path.order_label     , path.sec_order_label  ],
	f'{emj.EMJ_RAISING_HAND} Оператор'                      : ['oper_show' , simple_oper_ids_arr  , 'simple_oper'         ],
	f'{emj.EMJ_RAISING_HAND} Operator'                      : ['oper_show' , simple_oper_ids_arr  , 'simple_oper'         ],
	f'{emj.EMJ_DOCTOR} Доктор онлайн'                       : ['oper_show' , doctor_oper_ids_arr  , 'doc_oper'            ],
	f'{emj.EMJ_DOCTOR} Shifokor onlayn'                     : ['oper_show' , doctor_oper_ids_arr  , 'doc_oper'            ],
	f'{emj.EMJ_OLD_TELEPHONE} Тех. поддержка'               : ['oper_show' , support_oper_ids_arr , 'sup_oper'            ],
	f'{emj.EMJ_OLD_TELEPHONE} Тех. поддержка'               : ['oper_show' , support_oper_ids_arr , 'sup_oper'            ],
	f'{emj.EMJ_WRITING_HAND} Написать директору'            : ['oper_show' , director_oper_ids_arr, 'dir_oper'            ],
	f'{emj.EMJ_WRITING_HAND} Direktorga yozing'             : ['oper_show' , director_oper_ids_arr, 'dir_oper'            ],
	f'{emj.EMJ_BACK_ARROW} Отклонить вызов оператора'       : ['oper_close', 0                                            ],
	f'{emj.EMJ_BACK_ARROW} Operator chaqiruvini rad etish'  : ['oper_close', 1                                            ],
	f'{emj.EMJ_RAISING_HAND} Операторская'                  : ['redirect'  , 'к оператору'    , simple_oper_ids_arr  , 'simple_oper'],
	f'{emj.EMJ_OLD_TELEPHONE} Поддержка'                    : ['redirect'  , 'в тех.поддержку', support_oper_ids_arr , 'sup_oper'   ],
	f'{emj.EMJ_WRITING_HAND} Директор'                      : ['redirect'  , 'к директору'    , director_oper_ids_arr, 'dir_oper'   ],
	f'{emj.EMJ_DOCTOR} Доктор'                              : ['redirect'  , 'к доктору'      , doctor_oper_ids_arr  , 'doc_oper'   ]
}

markup_change_label_arr = [
	["FAQ текст"                           ,  "FAQ текст"                      ],
	["Текст отзыва"                        ,  "Текст отзыва"                   ],
	["Текст скидки"                        ,  "Текст скидки"                   ],
	["Текст адресса"                       ,  "Текст адресса"                  ],
	["Текст телефона"                      ,  "Текст телефона"                 ],
	["Начальный текст"                     ,  "Начальный текст"                ],
	["Текст оператора"                     ,  "Текст оператора"                ],
	["Текст создания заказа"               ,  "Текст создания заказа"          ],
	["Текст социальные сети"               ,  "Текст социальные сети"          ],
	["Текст инструкции оператора"          ,  "Текст инструкции оператора"     ]
]     

markup_change_collection_arr = [
	['Комментарий'                         ,   'Комментарий'                   ],
	['Данные по ПЦР'                       ,   'Данные по ПЦР'                 ],
	['Номер договора'                      ,   'Номер договора'                ],
	['Номер терминала'                     ,   'Номер терминала'               ],
	['Исправить наличные'                  ,   'Исправить наличные'            ],
	['Количество анализов'                 ,   'Количество анализов'           ],
	['Данные по ПЦР экспресс'              ,   'Данные по ПЦР экспресс'        ],
	['Информация по возврату средств'      ,   'Информация по возврату средств'],
]

office_markup_dict = {
	"МО Гор.больница №1"                   :   ['office'],
	"МО Кушбеги"                           :   ['office'],
	"МО  Мирзо Улугбека"                   :   ['office'],
	"МО  Юнусата"                          :   ['office'],
	"МО  viezd"                            :   ['office'],
	f"{emj.EMJ_BACK_ARROW} Назад"          :   ['office']
}