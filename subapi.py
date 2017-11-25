


import subprocess as sp
from threading import Thread

class SubApi:
    
    def __init__(self):
        self.outputListeners = set()
    
    
    def start(self, args, restartOnStop=True, listenDaemon=True):
        self.args = args
        self.restartOnStop = restartOnStop
        self.listenDaemon = listenDaemon
        self.program = sp.Popen(args, stdin=sp.PIPE, stdout=sp.PIPE, stderr=None, universal_newlines=True)
        
        self.t = Thread(target=self.listen, daemon=listenDaemon)
        self.t.start()
    
    
    def listen(self):
        while self.program.stdout.readable():
            outputLine = self.program.stdout.readline()[:-1]
            for listener in self.outputListeners:
                listener(outputLine)
    
    def sendInput(self, command):
        self.program.poll()
        #print(self.program.returncode)
        if self.program.returncode != None:
            self.program.stdout.close()
            if self.restartOnStop:
                self.start(self.args, self.restartOnStop, self.listenDaemon)
        self.program.stdin.write(command+"\n")
        try:
            self.program.stdin.flush()
        except Exception as err:
            print(err)
    
    def stop(self):
        self.program.terminate()
        self.program.stdout.close()


    
