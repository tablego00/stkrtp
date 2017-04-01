'''
Created on 2017/2/25

@author: ych
'''
import os,sys
import StockAT
from configparser import ConfigParser

class AppUtil:

    __instance__ = None

    PROJ_ROOT = os.path.dirname(StockAT.__file__).replace('\\','/')
    SETTINGS = PROJ_ROOT + '/resource/conf/settings.conf'
    config = ConfigParser()
    config.read(SETTINGS,encoding='utf-8')
    
    def __new__(cls):
        if not AppUtil.__instance__:
            AppUtil.__instance__ = object.__new__(cls)
        return AppUtil.__instance__

    def getStockMIS(self):
        return(self.config['TWSE']['STOCK_MIS'])
    
    def getStockRealTimePrice(self):
        return(self.config['TWSE']['RT_PRICE'])

    def getStockIDs(self):
        return(self.config['STATIC']['STOCKIDs'])

    def getLineChannelSecret(self):
        return(self.config['StoMonBot']['CHANNEL_SECRET'])
    
    def getLineChannelAccessToken(self):
        return(self.config['StoMonBot']['CHANNEL_ACCESS_TOKEN'])
    