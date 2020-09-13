from config.parcelList import saveParcelList, loadParcelList
from config.telegramBot import updater, dispatcher, CommandHandler
from model.parcel import Parcel

def track(update, context):
    print(f"went into track with {context.args}")
    if len(context.args) == 2:
        #try
            print("before freshpack")
            try:
                freshPack = Parcel(context.args[0], context.args[1], update.message.from_user["id"])
            except Exception as e:
                print(e.text)
            print(freshPack + " = " + freshPack.tracking)
            for elem in PARCEL_LIST:
                if(elem.tracking == freshPack.tracking):
                    context.bot.send_message(chat_id=update.message.chat_id, text=f"Das Paket wird schon getrackt! \n {freshPack}")
                    return
            PARCEL_LIST.append(freshPack)
            saveParcelList(PARCEL_LIST)
            context.bot.send_message(chat_id=update.message.chat_id, text=f"Paket erfolgreich hinzugefügt! \n {freshPack}")
        #except Exception as E:
            #print(E.text)
            #context.bot.send_message(chat_id=update.message.chat_id, text="Irgendwas ist schief gelaufen mit dieser Nummer: " + context.args[0])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Bitte sende mir deine DPD Trackingnummer und einen Namen (Format: /track NUMMER PACKETNAME)")

def remove(update, context):
    if context.args:
        try:
            user = update.message.from_user["id"]
            criteria = context.args[0]
            for elem in PARCEL_LIST:
                if (elem.owner == user) and (elem.alias == criteria):
                    context.bot.send_message(chat_id=update.message.chat_id, text=f"Folgendes Paket entfernt: \n {elem}")
                    PARCEL_LIST.remove(elem)
                    saveParcelList(PARCEL_LIST)
                    return
            context.bot.send_message(chat_id=update.message.chat_id, text=f"Paket mit Alias {criteria} wurde nicht gefunden!")
        except Exception as E:
            print(E.text)
            context.bot.send_message(chat_id=update.message.chat_id, text="Irgendwas ist schief gelaufen ...")
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Bitte sende mir den Alias des Paketes was du entfernen willst (/remove deinPaketName).")

def update(update, context):
    user = update.message.from_user["id"]
    updateFound = False
    for elem in PARCEL_LIST:
        if(elem.owner == user):
            if(elem.doUpdate()):
                updateFound = True
                context.bot.send_message(chat_id=update.message.chat_id, text=f"UPDATE! {elem}")
    if(not updateFound):
        context.bot.send_message(chat_id=update.message.chat_id, text="Leider hat sich nichts bewegt...")
    else:
        saveParcelList(PARCEL_LIST)
    

def getall(update, context):
    user = update.message.from_user["id"]
    isEmpty = True
    for elem in PARCEL_LIST:
        if(elem.owner == user):
            isEmpty = False
            context.bot.send_message(chat_id=update.message.chat_id, text=f"{elem}")
    if(isEmpty):
        context.bot.send_message(chat_id=update.message.chat_id, text=f"Du hast noch keine Pakete in deiner Liste. Nutze /track")

if __name__ == '__main__':
    # print all parcels currently tracked
    PARCEL_LIST = loadParcelList()
    for elem in PARCEL_LIST:
        print(elem)
    # deploy dispatcher
    dispatcher.add_handler(CommandHandler("track", track))
    dispatcher.add_handler(CommandHandler("update", update))
    dispatcher.add_handler(CommandHandler("getall", getall))
    dispatcher.add_handler(CommandHandler("remove", remove))
    updater.start_polling()