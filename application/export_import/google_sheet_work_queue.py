from threading import Thread
from multiprocessing import Queue

import logging
import traceback
from dataentry.models.interception_record import InterceptionRecord
from dataentry.models.story import Story
from export_import.google_sheet_basic import GoogleSheetBasic
from export_import.google_sheet import GoogleSheet
from dataentry.models.victim_interview import VictimInterview
from dataentry.dataentry_signals import irf_done, vif_done

logger = logging.getLogger(__name__);

class GoogleSheetWorkQueue(Thread):
    instance = None
    have_credentials = False
    const_irf = 'IRF'
    const_vif = 'VIF'
    const_shutdown = 'SHUTDOWN'
    const_work_type = 'WORK_TYPE'
    const_form_number = 'FORM_NUMBER'
    const_try_count = 'TRY_COUNT'
    const_create_story = 'CREATE_STORY'
    
    def __init__(self):
        try:
            logger.debug("In __init__") 
            self.irf_sheet = GoogleSheet.from_settings('IRF')
            logger.debug("Returned for allocating IRF have_credentails=" + str(self.irf_sheet.credentials)) 
            self.vif_sheet = GoogleSheet.from_settings('VIF')
            logger.debug("Returned from allocating VIF have_credentails=" + str(self.vif_sheet.credentials)) 
            self.irf_story_sheet = GoogleSheet.from_settings('IRF_STORY')
            self.story_sheet = GoogleSheetBasic.from_settings('STORY', tag='read')
            if self.irf_sheet.credentials and self.vif_sheet.credentials:
                logger.debug("have credentials")
                Thread.__init__(self)
                self.have_credentials = True
                self.work_queue = Queue()
                self.daemon = True
                self.start()
            else:
                logger.warn("Missing credentials")
        except:
            logger.warn("Exception thrown " + traceback.format_exc())
    
    def reinitialize(self):
        self.irf_sheet.get_sheet_metadata()
        self.vif_sheet.get_sheet_metadata()

    def run(self):
        while True:
            work = self.work_queue.get()
            
            if GoogleSheetWorkQueue.const_work_type not in work:
                logger.error(GoogleSheetWorkQueue.const_work_type + " not present in queue entry")
                continue
            else:
                work_type = work[GoogleSheetWorkQueue.const_work_type]
            
            if work_type != GoogleSheetWorkQueue.const_shutdown and GoogleSheetWorkQueue.const_form_number not in work:
                logger.error(GoogleSheetWorkQueue.const_form_number + " not present in queue entry for work type " + work_type)
                continue
            else:
                if GoogleSheetWorkQueue.const_form_number in work:
                    form_number = work[GoogleSheetWorkQueue.const_form_number]
                else:
                    form_number = 'N/A'
            
            if work_type != GoogleSheetWorkQueue.const_shutdown and GoogleSheetWorkQueue.const_try_count not in work:
                logger.error(GoogleSheetWorkQueue.const_try_count + " not present in queue entry for work type " + work_type)
                continue
            else:
                if GoogleSheetWorkQueue.const_try_count in work:
                    try_count = work[GoogleSheetWorkQueue.const_try_count]
                else:
                    try_count = 999
            
            if GoogleSheetWorkQueue.const_create_story in work:
                create_story = work[GoogleSheetWorkQueue.const_create_story]
            else:
                create_story = False
               
            logger.info("in run " + work_type + ", " + form_number)
            try:
                if work_type == GoogleSheetWorkQueue.const_irf:
                    self.internal_update_irf(form_number, create_story)
                elif work_type == GoogleSheetWorkQueue.const_vif:
                    self.internal_update_vif(form_number)
                elif work_type == GoogleSheetWorkQueue.const_shutdown:
                    self.work_queue.close()
                    self.have_credentials = False
                    return
                else:
                    logger.error("Unknown work type " + work_type)
            except:
                logger.error("Failed to process " + work_type + " " + form_number + " create story = " +str(create_story) + " on attempt " + str(try_count))
                self.reinitialize();
                try_count = try_count + 1
                if try_count < 2:
                    logger.error("GoogleSheetWorkQueue.run Failed to process " + work_type + " " + form_number + " on attempt " + str(try_count) + " - retrying")
                    work[GoogleSheetWorkQueue.const_try_count] = try_count
                    self.work_queue.put(work);
                else:
                    logger.error("GoogleSheetWorkQueue.run Failed to process " + work_type + " " + form_number + " on attempt " + str(try_count) + " - giving up\n" + traceback.format_exc())
                    self.send_exception_mail(traceback.format_exc())
                    break
    
    def internal_update_irf(self, the_irf_number, create_story):
        irf = None
        try:
            irf = InterceptionRecord.objects.get(irf_number = the_irf_number)            
        except:
            logger.info("Could not find IRF " + the_irf_number)
    
        self.irf_sheet.update(the_irf_number, irf)
        
        if create_story:
            logger.debug("creating stories for " + the_irf_number)
            mapped_data = self.irf_story_sheet.get_mapped_data(irf, 4)
            if mapped_data != None and len(mapped_data) > 0:
                victim_count = len(mapped_data)
                # build up 12 rows - the maximum number of victims in an IRF
                for pad_rows in range(12 - victim_count):
                    row = []
                    for pad_cols in range(len(mapped_data[0])):
                        row.append('')
                    mapped_data.append(row)
                
                self.irf_story_sheet.update_cells(2,4,13, len(mapped_data[0])+4, mapped_data)
                
                story_texts = self.story_sheet.get_data(2,0,victim_count + 1,0)
                print story_texts
                story_idx = 0
                for interceptee in irf.interceptees.all():
                    if interceptee.kind != "t":
                        if story_idx < len(story_texts):
                            if len(story_texts[story_idx][0].strip()) > 0:
                                story = Story()
                                story.interceptee = interceptee
                                story.story = story_texts[story_idx][0].strip()
                                story.save()
                            story_idx += 1


    def internal_update_vif(self, the_vif_number):
        vif = None
        try:
            vif = VictimInterview.objects.get(vif_number = the_vif_number)
        except:
            logger.info("Could not find VIF " + the_vif_number)
        
        self.vif_sheet.update(the_vif_number, vif)
        
    @staticmethod
    def update_form(form_number, form_type, create_story):
        try:
            logger.debug("form_number=" + form_number + ", form_type=" + form_type)
            if GoogleSheetWorkQueue.instance is None:
                GoogleSheetWorkQueue.instance = GoogleSheetWorkQueue()
            
            logger.debug("Back from creating GoogleSheetWorkQueue")
    
            if GoogleSheetWorkQueue.instance.have_credentials:
                work = {}
                work[GoogleSheetWorkQueue.const_work_type] = form_type
                work[GoogleSheetWorkQueue.const_form_number] = form_number
                work[GoogleSheetWorkQueue.const_create_story] = create_story
                work[GoogleSheetWorkQueue.const_try_count] = 0
                GoogleSheetWorkQueue.instance.work_queue.put(work)
                logger.debug("added to work queue form type=" + form_type + "form number=" + form_number)
            else:
                logger.debug("No credentials")
        except:
            logger.warn("Exception thrown " + traceback.format_exc())
        
    @staticmethod
    def handle_irf_done_signal(sender, **kwargs):
        logger.debug("Enter handle_irf_done_signal")
        irf_number = kwargs.get("irf_number")
        should_create_story = False
        if 'create_story' in kwargs:
            should_create_story = True
        logger.debug ("create_story=" + str(should_create_story) + " " + irf_number)
        GoogleSheetWorkQueue.update_form(irf_number, GoogleSheetWorkQueue.const_irf, should_create_story)
        
    @staticmethod
    def handle_vif_done_signal(sender, **kwargs):
        vif_number = kwargs.get("vif_number")
        GoogleSheetWorkQueue.update_form(vif_number, GoogleSheetWorkQueue.const_vif, False)
        
irf_done.connect(GoogleSheetWorkQueue.handle_irf_done_signal, weak=False, dispatch_uid="GoogleSheetWorkQueue")
vif_done.connect(GoogleSheetWorkQueue.handle_vif_done_signal, weak=False, dispatch_uid="GoogleSheetWorkQueue")
