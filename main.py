from config.parcelList import saveParcelList, loadParcelList
from config.telegramBot import updater, dispatcher, CommandHandler
from model.parcel import Parcel

def track(update, context):
    if context.args:
        try:
            freshPack = Parcel(context.args[0], context.args[1], update.message.from_user["id"])
            for elem in PARCEL_LIST:
                if(elem.tracking == freshPack.tracking):
                    context.bot.send_message(chat_id=update.message.chat_id, text=f"Das Paket wird schon getrackt! \n {freshPack}")
                    return
            PARCEL_LIST.append(freshPack)
            saveParcelList(PARCEL_LIST)
            context.bot.send_message(chat_id=update.message.chat_id, text=f"Paket erfolgreich hinzugefügt! \n {freshPack}")
        except:
            context.bot.send_message(chat_id=update.message.chat_id, text="Irgendwas ist schief gelaufen mit dieser Nummer: " + context.args[0])
    else:
        context.bot.send_message(chat_id=update.message.chat_id, text="Bitte sende mir deine DPD Trackingnummer und einen Namen (Format: /track NUMMER PACKETNAME)")


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
    for elem in PARCEL_LIST:
        if(elem.owner == user):
            context.bot.send_message(chat_id=update.message.chat_id, text=f"{elem}")

if __name__ == '__main__':
    # print all parcels currently tracked
    PARCEL_LIST = loadParcelList()
    for elem in PARCEL_LIST:
        print(elem)
    # deploy dispatcher
    dispatcher.add_handler(CommandHandler("track", track))
    dispatcher.add_handler(CommandHandler("update", update))
    dispatcher.add_handler(CommandHandler("getall", getall))
    updater.start_polling()