from django.shortcuts import render

# Create your views here.
from  .models import Malumotlar, Chat_ID

def home(request):


    from telegram.ext import Updater, Dispatcher, MessageHandler, ConversationHandler,\
        CallbackContext, CommandHandler,  Filters
    from telegram import Update, ReplyKeyboardMarkup , ReplyKeyboardRemove, KeyboardButton, MessageEntity

    updater: Updater = Updater(token='5033183715:AAH32sWrautN1rTnL4oGCnHu_tFAJ5HvevQ')

    dispatcher  =  updater.dispatcher



    MENU_STATE, MUROJAT_STATE, MUROJAT_STATE2, FULL_NAME_STATE, PHONE_STATE, FIKR_STATE, MATN_STATE = range(7)

    print("ishga tushdi")


    def murojot3():
        return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📝Murojat Yo'lash📝"),
                KeyboardButton(text="📒Mening Murojatlarim📒")
            ],
            [
                KeyboardButton(text="🔐Hemis Parolni tiklash🔐")
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    def matn_send_or_canel():
        return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="✅Yuborish✅")
            ],
            [
                KeyboardButton(text="❌Bekor qilish❌")
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )

    def  who():
        return ReplyKeyboardMarkup(
        keyboard = [
            [
                KeyboardButton(text="👨‍🎓 Talaba"),
                KeyboardButton(text="👨‍👩‍👧 Ota ona"),
            ],
            [
                KeyboardButton(text="👨‍💼 Xodimlar"),
                KeyboardButton(text="Boshqa"),
            ],
        
        ],
        resize_keyboard=True, one_time_keyboard=True
    )


    def murojat():
        return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Shikoyat", callback_data="shikoyat"),
                KeyboardButton(text="Taklif", callback_data="taklif"),

            ],
            [
                KeyboardButton(text="Ariza", callback_data="ariza"),
                KeyboardButton(text="Boshqa", callback_data="boshqa"),
            ],
            [
                KeyboardButton(text="🔙Orqaga")
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )



    def murojat2():
        return ReplyKeyboardMarkup(
        keyboard=[
        
            [
                KeyboardButton(text="REKTORAT", callback_data="shikoyat"),
                KeyboardButton(text="Korupsiyaga qarshi", callback_data="taklif"),

            ],
            [
                KeyboardButton(text="Foydali qazilma konlari geologiyasi fakulteti ", callback_data="ariza"),
            ],
            [
            KeyboardButton(text="Neft va gaz konlari geologiyasi fakulteti", callback_data="boshqa"),
            ],
            [
                KeyboardButton(text="🔙Orqaga")
            ]
            
        ],
        resize_keyboard=True, one_time_keyboard=True
    )



    def my_contact():
        return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Telofon raqam",
                request_contact=True)
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )



    def ishga_tushdi(update:Update, context:CallbackContext):
        msg  =  "botni ishga tushirish uchun👉 /start 👈 bosing"
        a = Chat_ID.objects.all()
        if len(a) == 0:
            update.message.reply_text("Foydalanuvchilar mavjud emas ")
        else:
            for i in a:
                
                context.bot.send_message(chat_id=i.chat_id, text=msg)
                print(i.chat_id)
        return MENU_STATE



    def start_handler(update:Update, context:CallbackContext):
        update.message.reply_text("Assalom alaykum GFU murojat botga xush kelibsiz !!!", reply_markup=murojot3())
        a = update.message.chat['id']
        b = Chat_ID.objects.filter(chat_id = a)

        if len(b) == 0:
            Chat_ID.objects.create(
                chat_id  = a,
            )
            print("saqlandi")
        
        return MENU_STATE
        return MENU_STATE



    def menu_handler(update:Update, context:CallbackContext):

        update.message.reply_text("Murojat yo'lash uchun tugmani bosing", reply_markup=murojot3())

    def murojat_yolash_handler(update:Update , context:CallbackContext):
        update.message.reply_text(
            'Siz kimsiz ???', reply_markup=who()
        )


            
        return MUROJAT_STATE




    def murojat_handler(update:Update, context:CallbackContext):
    
        update.message.reply_text("👇👇Bo'limni Tanglang👇👇", reply_markup=murojat())
        if update.message.text == '🔙Orqaga':
            print("2_______________________________2")
            return menu_handler(update, context)
            
            
        context.chat_data.update({
            "shaxs":update.message.text
        })
        print(context.chat_data)
        return MUROJAT_STATE2
    def murojat_resend_handler(update:Update, context:CallbackContext):
        update.message.reply_text("👇👇Bo'limni Tanglang👇👇", reply_markup=murojat())
    
            
            
        context.chat_data.update({
            "shaxs":update.message.text
        })
        print(context.chat_data)
        return MUROJAT_STATE2

    def murojat2_handler(update:Update, context:CallbackContext):
        
        if update.message.text == '🔙Orqaga':
            print("3______________________________3")
            return murojat_yolash_handler(update, context)
        update.message.reply_text("👇👇Murojat kimga👇👇", reply_markup=murojat2())

        context.chat_data.update({
            "Bolim":update.message.text
        })

        return FULL_NAME_STATE

    def full_name_hanler(update:Update, context:CallbackContext):
        if update.message.text == '🔙Orqaga':
            return murojat_resend_handler(update, context)
        update.message.reply_text("✍️Ism Familyangizni kiriting✍️:", reply_markup=ReplyKeyboardRemove())
        context.chat_data.update({
            "Kimga":update.message.text
        })
        return PHONE_STATE

    def phone_entity_handler(update:Update, context:CallbackContext):
        phone_number_entity = pne = \
        list(filter(lambda e: e.type == 'phone_number', update.message.entities))[0]
    
        phone_number  = update.message.text[pne.offset:pne.offset + pne.length]
        context.chat_data.update({
            'phone_number':phone_number
        })
        update.message.reply_text("🖌Murojatingizni Yozing🖌")
        return FIKR_STATE

    def phone_contact_handler(update:Update, context:CallbackContext):
        contact =  update.message.contact
        context.chat_data.update({
            'phone_number':contact.phone_number
        })
        update.message.reply_text("🖌Murojatingizni Yozing🖌")
        return FIKR_STATE
    def feedback_handler(update:Update, context:CallbackContext):
        
        context.chat_data.update({
            "Fikr":update.message.text
        })
        a = context.chat_data
        update.message.reply_text(f"Murojatingiz uchun tashakur !! Sizning {a['Bolim']}")
        update.message.reply_text(f"👨‍💼Shaxsi:{a['shaxs']}\n🧾Murojat turi:{a['Bolim']}\n👨‍💼Kimga:{a['Kimga']}\n🖊FISH:{a['full_name']}\n📱Telfon raqam:{a['phone_number']}\n📃Matni:{a['Fikr']} \n", reply_markup=matn_send_or_canel())

        return MATN_STATE


    def send_message_handler(update:Update, context:CallbackContext):
        a = context.chat_data
        msg = f"👨‍💼Shaxsi:{a['shaxs']}\n🧾Murojat turi:{a['Bolim']}\n👨‍💼Kimga:{a['Kimga']}\n🖊FISH:{a['full_name']}\n📱Telfon raqam:{a['phone_number']}\n📃Matni:{a['Fikr']} \n"
        Malumotlar.objects.create(
            full_name = a['full_name'][0:256],
            phone =  a['phone_number'][0:256],
            who = a['shaxs'][0:256],
            bolim = a['Bolim'][0:256],
            kimga = a['Kimga'][0:256],
            text = a['Fikr'][0:256],
            chat_id  = update.effective_user.id,
        )
        context.bot.send_message(chat_id=1858379541, text=msg)
        context.bot.send_message(chat_id=85942449, text=msg)
    
        update.message.reply_text("Murojatingiz yuborildi!!!", reply_markup=murojot3())
        
        return MENU_STATE

    def canel_message_handler(update:Update, context:CallbackContext):
        
        
        update.message.reply_text("Murojatingiz bekor qilindi!!!", reply_markup=murojot3())
        print(context.chat_data)
        return MENU_STATE




    def send_or_canel_handler(update:Update, context:CallbackContext):
        update.message.reply_text('👇👇Pasdagi tugmadan birini tanlang👇👇')
        

    def all_murojatlarim_handler(update:Update, context:CallbackContext):
        update.message.reply_text(
            "Oxirgi murojaatlarim ro'yhati", 
        )
        a =  Malumotlar.objects.order_by("-data").filter(chat_id = update.effective_user.id)
        if len(a) == 0:
            update.message.reply_text("Sizning Murojatlar hali mavjud emas !!!")
        else:
            for i in a:
                update.message.reply_text(f"📅Sana:{i.data}\n👨‍💼Shaxsi:{i.who}\n🧾Murojat turi:{i.bolim}\n👨‍💼Kimga:{i.kimga}\n🖊FISH:{i.full_name}\n📱Telfon raqam:{i.phone}\n📃Matni:{i.text}")

    



    ############################# RESEND #######################################
    def murojat_resend_handler(update:Update, context:CallbackContext):
        update.message.reply_text("👇👇Bo'limni Tanglang👇👇", reply_markup=murojat())

    def murojat2_resend_handler(update:Update, context:CallbackContext):
        update.message.reply_text("👇👇Murojat kimga👇👇", reply_markup=murojat2())

    def full_name_resend_handler(update:Update, context:CallbackContext):
        update.message.reply_text("✍️Ism Familyangizni kiriting✍️:", reply_markup=ReplyKeyboardRemove())
    
    def phone_resend_handler(update:Update, context:CallbackContext):
        context.chat_data.update({
            "full_name":update.message.text
        })
        update.message.reply_text("📞Telfon raqamingizni kiriting(+998 XXX-XX-XX): yoki pastdagi tugmani bosing", reply_markup=my_contact())
    
    def feedbeck_resend(update:Update, context:CallbackContext):
        update.message.reply_text("🖌Murojatingizni Yozing🖌")


    dispatcher.add_handler(ConversationHandler(
        
        entry_points=[
        
            CommandHandler('start', start_handler),
            ],
        states={
            MENU_STATE: [
                MessageHandler(Filters.regex(r"^📝Murojat Yo'lash📝$"), murojat_yolash_handler),
                MessageHandler(Filters.regex(r"📒Mening Murojatlarim📒"), all_murojatlarim_handler),
                MessageHandler(Filters.regex(r"/ishga_tushurish"), ishga_tushdi),
                MessageHandler(Filters.all, menu_handler),
                
            ],
            MUROJAT_STATE:  [
                
                MessageHandler(Filters.text, murojat_handler),
                MessageHandler(Filters.all, murojat_yolash_handler),
            ],
            MUROJAT_STATE2: [
                MessageHandler(Filters.text, murojat2_handler),
                MessageHandler(Filters.all, murojat2_resend_handler),
            ],
            FULL_NAME_STATE:[
                MessageHandler(Filters.text, full_name_hanler),
                MessageHandler(Filters.all, full_name_resend_handler),
            ],
            PHONE_STATE:[ 
                MessageHandler(Filters.text & Filters.entity(MessageEntity.PHONE_NUMBER), phone_entity_handler),
                MessageHandler(Filters.contact, phone_contact_handler),
                MessageHandler(Filters.all, phone_resend_handler),
            ], 
            FIKR_STATE: [ 
                MessageHandler(Filters.text, feedback_handler),
                MessageHandler(Filters.all, feedbeck_resend),
            ],
            MATN_STATE: [ 
                MessageHandler(Filters.regex(r"^✅Yuborish✅$"), send_message_handler),
                MessageHandler(Filters.regex(r"^❌Bekor qilish❌$"), canel_message_handler),
                MessageHandler(Filters.all, send_or_canel_handler)
            ],

        },
        fallbacks=[],
    ))








    updater.start_polling()
    updater.idle()