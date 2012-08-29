# RandomGametypeUrT Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.0'

import b3
import b3.plugin
import b3.events
import random
import b3, time, threading, thread

def gametype(cgametype):

    if cgametype=="ffa":
    
        ngametype = 0
        mgametype='FreeForAll'
    
    if cgametype=="lms":
        
        ngametype = 1   
        mgametype='LastManStanding'

    if cgametype=="tdm":
        
        ngametype = 3     
        mgametype='TeamDeathMatch'

    if cgametype=="ts":
        
        ngametype = 4 
        mgametype='Team Survivor'

    if cgametype=="ftl":
         
        ngametype = 5 
        mgametype='Follow the Leader'

    if cgametype=="cah":
           
        ngametype = 6  
        mgametype='Capture and Hold'

    if cgametype=="ctf":

        ngametype = 7 
        mgametype='Capture The Flag'
        
    if cgametype=="bomb":

        ngametype = 8
        mgametype='Bombmode'

    return ngametype, mgametype

class RandomgametypeurtPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _adminlevel = 100
    _gametypes = "ffa lms tdm ts ctf bomb ftl cah"
    _swaproleson = "bomb"
    _rgonoff = "off"
    _test = None

    def onStartup(self):

        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False
        
        self.registerEvent(b3.events.EVT_GAME_MAP_CHANGE)

        self._adminPlugin.registerCommand(self, 'randomgametype',self._adminlevel, self.cmd_randomgametype)

    def onLoadConfig(self):

        try:
            self._adminlevel = self.config.getint('settings', 'adminlevel')
        except Exception, err:
            self.warning("Using default value %s for adminlevel. %s" % (self._adminlevel, err))
        self.debug('min level for cmds : %s' % self._adminlevel)

        try:
            self._gametypes = self.config.get('settings', 'gametypes')
        except Exception, err:
            self.warning("Using default value %s for gametypes. %s" % (self._gametypes, err))
        self.debug('gametypes : %s' % self._gametypes)

        try:
            self._swaproleson = self.config.get('settings', 'swaproleson')
        except Exception, err:
            self.warning("Using default value %s for swaproleson. %s" % (self._swaproleson, err))
        self.debug('swaproleson : %s' % self._swaproleson)

        try:
            self._rgonoff = self.config.get('settings', 'pluginactived')
        except Exception, err:
            self.warning("Using default value %s for pluginactived. %s" % (self._rgonoff, err))
        self.debug('pluginactived : %s' % self._rgonoff)


    def onEvent(self, event):
        
        if event.type == b3.events.EVT_GAME_MAP_CHANGE:

            if self._rgonoff == "on":

                self.randomgametype()
    
    def cmd_randomgametype(self, data, client, cmd=None):
        
        """\
        activate / deactivate randomgametypeurt
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._rgonoff == 'on':

                client.message('RandomGametypeUrT ^2activated')

            if self._rgonoff == 'off':

                client.message('RandomGametypeUrT ^1deactivated')

            client.message('!randomgametype <on / off>')
            return

        if input[0] == 'on':

            if self._rgonoff != 'on':

                self._rgonoff = 'on'
                message = '^2activated'

            else:

                client.message('RandomGametypeUrT is already ^2activated') 

                return False

        if input[0] == 'off':

            if self._rgonoff != 'off':

                self._rgonoff = 'off'
                message = '^1deactivated'

            else:
                
                client.message('RandomGametypeUrT is already ^1disabled')                

                return False

        client.message('RandomGametypeUrT %s'%(message))

    def randomgametype(self):

        self.grandom()

        lgametype = gametype(self.nextgametype)
        ngametype = lgametype[0]
        self.mgametype = lgametype[1] 

        thread.start_new_thread(self.wait, (60,))

        self.console.write("g_gametype %s"%(ngametype))

        if self.nextgametype in self._swaproleson:
        
            self.console.write("g_swaproles 1")

        else:

            self.console.write("g_swaproles 0")
    
    def grandom(self):

        ngametype = 0

        self.listgametype = self._gametypes.split(' ')

        for gametype in self.listgametype:
            ngametype += 1

        nagametype = random.randint(0, ngametype-1)

        x = nagametype
        self.nextgametype = self.listgametype[x]

        return

    def wait(self, temps):

        time.sleep(temps)
          
        self.console.write('bigtext "^2Random Next Gametype: ^4%s^7"'%self.mgametype)
