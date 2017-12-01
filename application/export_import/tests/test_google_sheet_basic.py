import os
from django.test import TestCase

from export_import.google_sheet_basic import GoogleSheetBasic

class GoogleSheetBasicTest(TestCase):
    def setUp(self):
        # save Google sheet credential file configuration and reset it to the
        # test credentials
        self.save_cred = os.environ['GOOGLE_APPLICATION_CREDENTIALS']
        os.environ['GOOGLE_APPLICATION_CREDENTIALS']='/data/etc/google_cred.json'
        
        self.sourceSheet = GoogleSheetBasic.from_settings('TEST_GoogleSheetExportBase', 'edit')
        self.destSheet = GoogleSheetBasic.from_settings('TEST_GoogleSheetBasic', 'edit')
        
        data = self.sourceSheet.get_data(1, 0, self.sourceSheet.rowCount, self.sourceSheet.colCount)
        
        reqs = []
        reqs.append(self.destSheet.delete_request(1, self.destSheet.rowCount-1))
        reqs.append(self.destSheet.expand_request(self.sourceSheet.rowCount))
        reqs.append(self.destSheet.delete_request(0, 0))
        self.destSheet.batch_update(reqs)
        
        self.destSheet.append_rows(data)
    
    def tearDown(self):
        TestCase.tearDown(self)
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = self.save_cred
    
    def test_convert(self):
        self.assertEqual('A200', self.destSheet.convert_notation(200,0))
        self.assertEqual('Z200', self.destSheet.convert_notation(200,25))
        self.assertEqual('AA199',self.destSheet.convert_notation(199,26))
        self.assertEqual('KB199',self.destSheet.convert_notation(199,287))
        
    def test_row_count(self):
         self.assertEqual(self.destSheet.rowCount, self.sourceSheet.rowCount)
        
    def test_delete(self):
        reqs = []
        reqs.append(self.destSheet.delete_request(3,4))
        self.destSheet.batch_update(reqs)
        
        #verify in memory row count
        self.assertEqual(self.destSheet.rowCount, self.sourceSheet.rowCount - 2, msg='In memory value')
        
        #refresh count from google sheet
        self.destSheet.get_sheet_metadata()
        self.assertEqual(self.destSheet.rowCount, self.sourceSheet.rowCount - 2, msg='Refresh from google sheet')
    
    def test_expand_request(self):
        reqs = []
        reqs.append(self.destSheet.expand_request(101))
        self.destSheet.batch_update(reqs)
        
        #verify in memory row count
        self.assertEqual(self.destSheet.rowCount, self.sourceSheet.rowCount + 101, msg='In memory value')
        
        #refresh count from google sheet
        self.destSheet.get_sheet_metadata()
        self.assertEqual(self.destSheet.rowCount, self.sourceSheet.rowCount + 101, msg='Refresh from google sheet')
    
    def test_get_data(self):
        data = self.destSheet.get_data(1, 0, self.destSheet.rowCount, self.destSheet.colCount-1)
        self.assertEqual(len(data), self.destSheet.rowCount)
        self.assertEqual(len(data[0]), self.destSheet.colCount)
        self.assertEqual('Test21', data[1][1])
        self.assertEqual('Test52', data[4][2])
    
    def test_update_cell(self):
        self.destSheet.update_cell(3,1,'TestUpdate')
        data = self.destSheet.get_data(1, 0, self.destSheet.rowCount, self.destSheet.colCount-1)
        self.assertEqual('TestUpdate', data[2][1])
    
    def test_update_cells(self):
        new_data = [['TestUpd21','UpdateTest22'],['TestUpd31','UpdateTest32']]
        
        self.destSheet.update_cells(2,1,3,2, new_data)
        data = self.destSheet.get_data(1, 0, self.destSheet.rowCount, self.destSheet.colCount-1)
        self.assertEqual('TestUpd21', data[1][1])
        self.assertEqual('UpdateTest32', data[2][2])
    
    def test_zappend_rows(self):
        new_data = [['EFG', 'Test61','Test62'],['FGH','Test71','Test72']]
        reqs=[]
        reqs.append(self.destSheet.expand_request(2)) 
        self.destSheet.batch_update(reqs)
        
        self.destSheet.append_rows(new_data)
        self.assertEqual(self.destSheet.rowCount, self.sourceSheet.rowCount + 2, msg='In memory value')
        data = self.destSheet.get_data(1, 0, self.destSheet.rowCount, self.destSheet.colCount-1)
        self.assertEqual('Test62', data[self.destSheet.rowCount-2][self.destSheet.colCount-1])
        self.assertEqual('FGH', data[self.destSheet.rowCount-1][0])
       
    