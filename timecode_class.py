class Timecode_Parser():
    def __init__(self, timecode: str, framerate: float, df:bool =False):
        self.smpte = timecode
        
        self.drop_frame = df

        # Technically 29.97 should be drop frame, but it's not working that way with the files I tested. Pending to fix or not
        if len(self.smpte.split(';')) >= 2:
            self.drop_frame = True


        if framerate == 29.97 or framerate ==  23.976 or framerate ==  24.0 or framerate ==  25.0 or framerate ==  30.0:
            #self.drop_frame = True
            self.int_framerate = int(round(framerate))
            self.framerate = float(framerate)
        else:
            raise ValueError('Invalid framerate')
        

        # Drop frames is the 6% of the framerate rounded to the nearest number. Confirm this formula

        # I get the 0.06666 * framerate to calculate the drop frames from here https://www.davidheidelberger.com/2010/06/10/drop-frame-timecode/
        if self.drop_frame or len(self.smpte.split(';')) >= 2:
            self.drop_frames = int(round(self.framerate * 0.0666666))
        else:
            self.drop_frames = 0

        self.total_frames = self.linear_timecode_total_frames()

        self.real_time = 0

        self.timecode = self.smpte_to_real_time()

    def printer(self):
        print(self.smpte, self.timecode)


    def linear_timecode_total_frames(self):
        #hour_frames = self.int_framerate * 60 * 60
        if len(self.smpte.split(';')) >= 2:
            hours, minutes, seconds = self.smpte.split(':')
            seconds, frames = seconds.split(';')

        else:
            hours, minutes, seconds, frames = self.smpte.split(':')

        try:
            total_minutes = (60 * int(hours)) / int(minutes)
        except:
            total_minutes = 0
        

        total_frames = (((int(hours) * 3600) + (int(minutes) * 60) + int(seconds)) * self.int_framerate) + int(frames) - (self.drop_frames * (total_minutes - (total_minutes // 10)))

        return total_frames
    
    def smpte_to_real_time(self):

        miliseconds = int((self.total_frames / self.framerate ) * 1000)

        hours = miliseconds // (1000 * 60 * 60)
        minutes = (miliseconds // (1000 * 60)) % 60
        seconds = (miliseconds // 1000) % 60
        miliseconds = miliseconds % 1000

        return '0{}:{:02d}:{:02d},{:03d}'.format(hours, minutes, seconds, miliseconds)


