import json
from pathlib import Path

class Config:
    def __init__(self,path="config.json"):
        self.path=Path(path)
        self.defaults={
            "folder":"",
            "interval":3,
            "position":"fill"
        }
        self.validPositions={
            "center","tile",
            "stretch","fit",
            "fill"
        }

    def load(self):
        if not self.path.exists():
            self.save(self.defaults)
            return self.defaults.copy()

        try:
            with open(self.path,"r") as file:
                config=json.load(file)
        
        except(json.JSONDecodeError,OSError):
            print("Invalid config file. Using Defaults")
            return self.defaults.copy()
        return self.validate(config)

    def validate(self,config):
        result=self.defaults.copy()

        folder=config.get("folder")

        if( isinstance(folder,str) and folder and Path(folder).is_dir()):
            result["folder"]=folder

        interval=config.get("interval")
        if(isinstance(interval,(int,float)) and interval>0):
            result["interval"]=interval

        position=config.get("position")
        if(isinstance(position,str) and position.lower() in self.validPositions):
            result["position"]=position.lower()

        return result

    def save(self,config):
        with open(self.path,"w") as file:
            json.dump(config,file,indent=4)