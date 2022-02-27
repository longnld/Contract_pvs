from cgitb import text
#from turtle import update
from typing import DefaultDict
import pdfplumber
import io
import re
import ast
def read(filename):

	pdf = pdfplumber.open(filename)#
	total_pages = len(pdf.pages) #Đọc số trang file pdf
	#print(total_pages)

	list_table=[]
	if total_pages == 1:
		page = pdf.pages[0]#Đọc trang đầu tiên
		text = page.extract_text() #Lấy dữ liệu text từ trang đầu
	elif total_pages > 1:
		text=''
		for i in range(total_pages):
			page_i=pdf.pages[i]			
			if page_i is not None : 
				#print(page_i)
				#print("-------------------------------------------------------------------")
				tables = page_i.find_tables()
				#print(tables)

				if tables != []:
					for i in tables:
						for x in i.extract(x_tolerance=5):
							if any(word in x for word in ["TT","Danh mục"]):
								list_table.append(i.extract(x_tolerance=5))
				text_i=page_i.extract_text()
				text+=text_i
		#print(text.count("TT"))	
	#print(text)
	#print(list_table)
	new_list_table=[]
	for list_1 in list_table:
		new_list=[]
		for list_2 in list_1:
			list_2 = [ ele for ele in list_2 if ele not in [None,'','\n'] ]
			#print(list_2)
			new_list.append(list_2)
		new_list_table.append(new_list)	
	#print(new_list_table)

	int_STT = list(range(1, 200)) #Tạo list STT từ 1 -> 199
	str_STT = list(map(str,int_STT)) #Convert list int thành list string

	list_content=[]
	if new_list_table != []:
		for list_1 in  new_list_table:
			list_content_iterable=[]
			for line in list_1:
				if any(word.strip() in line for word in str_STT):
					list_content_iterable.append(line[1])
			list_content.append(list_content_iterable)
			#print("-------------------")
	#print(list_content)
					
					
		#list_content.append(list_content1)
	#print(list_content)
#---------------------------------------------------------------------------------
# BỘ LỌC CHIA LAYOUT (CẬP NHẬT NẾU CÓ MẪU HÓA ĐƠN MỚI)
#---------------------------------------------------------------------------------
	#---------------------------------------------------------------------
	begin_ZONE_INFO 					= 		['HỢP ĐỒNG','Số:']
	
	end_ZONE_INFO 						= 		['Bên A','Người đại diện :']
	#------------------------------------------------------------
	begin_CONTRACTORS_A                 =['Bên A','Người đại diện :']
	
	end_CONTRACTORS_A                   =['Mã số thuế :']
	
	begin_CONTRACTORS_B                 =['Bên B']
	
	end_CONTRACTORS_B                   =['ĐIỀU 1: ']

	#-----------------------------------------------------------------
	begin_zone_CONTRACT_VALUE			=['GIÁ TRỊ HỢP ĐỒNG',"Giá trị hợp đồng:","PHƯƠNG THỨC THANH TOÁN"]
	end_zone_CONTRACT_VALUE				=['Thủ tục thanh toán','THANH TOÁN CHẬM VÀ ĐIỀU CHỈNH HÓA ĐƠN']
	begin_zone_SETUP					=['Chi phí lắp đặt : ','Chi phí lắp đặt:']
	end_zone_SETUP						=['Chi phí bảo trì :','Chi phí hàng tháng']
	begin_MONTHCOST                     =['Chi phí hàng tháng','Chi phí bảo trì :']
	end_MONTHCOST                       =['Thủ tục thanh toán']
	begin_zone_SETUP2					=['Chi phí đấu nối, hòa mạng (thanh toán 01 (một) lần):','Chi phí đấu nối, hòa mạng ']
	end_zone_SETUP2						=['Cước phí sử dụng dịch vụ Kênh MPLS','Cước phí sử dụng ',' dịch vụ Kênh MPLS']
	begin_zone_SETUP3					=["Cước phí sử dụng dịch vụ Kênh MPLS",'Cước phí sử dụng ',' dịch vụ Kênh MPLS']
	end_zone_SETUP3						=["ĐIỀU 4: THANH TOÁN CHẬM VÀ ĐIỀU CHỈNH HÓA ĐƠN",'ĐIỀU 4']

#-----------------------------------------------------------------------------
#---------------------------------------------------------------------------------

#VẼ LAYOUT HỢP ĐỒNG

#---------------------------------------------------------------------------------
	#ZONE_INFO
	begin_line_ZONE_INFO_list=[]
	if text is not None:
		for number,line in enumerate((text.splitlines()), 1):
			if any(word in line for word in begin_ZONE_INFO):
				begin_lines_ZONE_INFO=int(number)
				begin_line_ZONE_INFO_list.append(begin_lines_ZONE_INFO)
				#print(begin_lines_ZONE_INFO)

	if len(begin_line_ZONE_INFO_list)>0:
		begin_line_ZONE_INFO=min(begin_line_ZONE_INFO_list)
	else:
		begin_line_ZONE_INFO=None
	
	end_line_ZONE_INFO_list=[]
	if text is not None:
		for number,line in enumerate((text.splitlines()),1):
			if any(word in line for word in end_ZONE_INFO):
				end_lines_ZONE_INFO=int(number)
				end_line_ZONE_INFO_list.append(end_lines_ZONE_INFO)
				#print(end_lines_ZONE_INFO)
	
	if len(end_line_ZONE_INFO_list)>0:
		end_line_ZONE_INFO=min(end_line_ZONE_INFO_list)
	else:
		end_line_ZONE_INFO=None
	#print("begin"+str(begin_line_ZONE_INFO))
	#print("end"+str(end_line_ZONE_INFO))
	
	if begin_line_ZONE_INFO is not None and end_line_ZONE_INFO is not None:
		if begin_line_ZONE_INFO >1:
			ZONE_INFO=io.StringIO(text).readlines()[begin_line_ZONE_INFO-2:end_line_ZONE_INFO+3]

		else:
			ZONE_INFO=io.StringIO(text).readlines()[begin_line_ZONE_INFO-1:end_line_ZONE_INFO+3]
	else:
		ZONE_INFO=None


	#CONTRACTORS
	begin_line_CONTRACTORS_A_list=[]    
	
	if text is not None:
		for number,line in enumerate((text.splitlines()),1):
			if any(word in line for word in begin_CONTRACTORS_A):
				begin_lines_CONTRACTORS=int(number)
				begin_line_CONTRACTORS_A_list.append(begin_lines_CONTRACTORS)
	if len(begin_line_CONTRACTORS_A_list)>0:
		begin_line_CONTRACTORS=min(begin_line_CONTRACTORS_A_list)
	else:
		begin_line_CONTRACTORS=None

	end_line_CONTRACTORS_A_list=[]
	if text is not None:
		for number,line in enumerate((text.splitlines()),1):
			if any(word in line for word in end_CONTRACTORS_A):
				end_lines_CONTRACTORS=int(number)
				end_line_CONTRACTORS_A_list.append(end_lines_CONTRACTORS)
	if len(end_line_CONTRACTORS_A_list)>0:
		end_line_CONTRACTORS=min(end_line_CONTRACTORS_A_list)
	else:
		end_line_CONTRACTORS=None
	
	if end_line_CONTRACTORS is not None and begin_line_CONTRACTORS is not None:
		if begin_line_CONTRACTORS>1:
			Contractors_A=io.StringIO(text).readlines()[begin_line_CONTRACTORS-2:end_line_CONTRACTORS+1]
		else:
			Contractors_A=io.StringIO(text).readlines()[begin_line_CONTRACTORS-1:end_line_CONTRACTORS+1]
	else:
		Contractors_A=None
	#print(Contractors_A)

	begin_line_CONTRACTORS_B_list=[]
	if text is not None:
		for number,line in enumerate((text.splitlines()),1):
			if any(word in line for word in begin_CONTRACTORS_B):
				begin_lines_CONTRACTORS=int(number)
				begin_line_CONTRACTORS_B_list.append(begin_lines_CONTRACTORS)
	if len(begin_line_CONTRACTORS_B_list)>0:
		begin_line_CONTRACTORS=min(begin_line_CONTRACTORS_B_list)
	else:
		begin_line_CONTRACTORS=None

	end_line_CONTRACTORS_B_list=[]
	if text is not None:
		for number,line in enumerate((text.splitlines()),1):
			if any(word in line for word in end_CONTRACTORS_B):
				end_lines_CONTRACTORS=int(number)
				end_line_CONTRACTORS_B_list.append(end_lines_CONTRACTORS)
	if len(end_line_CONTRACTORS_B_list)>0:
		end_line_CONTRACTORS=min(end_line_CONTRACTORS_B_list)
	else:
		end_line_CONTRACTORS=None
	
	if end_line_CONTRACTORS is not None and begin_line_CONTRACTORS is not None:
		if begin_line_CONTRACTORS>1:
			Contractors_B=io.StringIO(text).readlines()[begin_line_CONTRACTORS:end_line_CONTRACTORS+3]
		else:
			Contractors_B=io.StringIO(text).readlines()[begin_line_CONTRACTORS:end_line_CONTRACTORS+3]
	else:
		Contractors_B=None
	#print(Contractors_B)

#Check giá trị hợp đồng
	begin_CONTRACT_VALUE_list=[]
	if text is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in begin_zone_CONTRACT_VALUE):
				begin_lines_CONTRACT_VALUE=int(number)
				begin_CONTRACT_VALUE_list.append(begin_lines_CONTRACT_VALUE)
	if len(begin_CONTRACT_VALUE_list)>0:
		begin_line_CONTRACT_VALUE=min(begin_CONTRACT_VALUE_list)
	else:
		begin_line_CONTRACT_VALUE=None
	end_CONTRACT_VALUE_list=[]
	if text is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in end_zone_CONTRACT_VALUE):
				end_lines_CONTRACT_VALUE=int(number)
				end_CONTRACT_VALUE_list.append(end_lines_CONTRACT_VALUE)
	if len(end_CONTRACT_VALUE_list)>0:
		end_line_CONTRACT_VALUE=min(end_CONTRACT_VALUE_list)
	else:
		end_line_CONTRACT_VALUE=None
	if end_line_CONTRACT_VALUE is not None and begin_line_CONTRACT_VALUE is not None:
		if begin_line_CONTRACT_VALUE>1:
			CONTRACT_VALUE=io.StringIO(text).readlines()[begin_line_CONTRACT_VALUE-1:end_line_CONTRACT_VALUE+3]
		else:
			CONTRACT_VALUE=io.StringIO(text).readlines()[begin_line_CONTRACT_VALUE-2:end_line_CONTRACT_VALUE+3]
	else:
		CONTRACT_VALUE=None
	#print(CONTRACT_VALUE)
	#check chi phí lắp đặt
	begin_zone_SETUP_list=[]
	if CONTRACT_VALUE is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in begin_zone_SETUP):
				begin_lines_setup=int(number)
				begin_zone_SETUP_list.append(begin_lines_setup)
	if len(begin_zone_SETUP_list)>0:
		begin_line_setup=min( begin_zone_SETUP_list)
	else:
		begin_line_setup=None
	end_zone_SETUP_list=[]
	if CONTRACT_VALUE is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in end_zone_SETUP):
				end_lines_setup=int(number)
				end_zone_SETUP_list.append(end_lines_setup)
	if len(end_zone_SETUP_list)>0:
		end_line_setup=min( end_zone_SETUP_list)
	else:
		end_line_setup=None
	if end_line_setup is not None and begin_line_setup is not None:
		if begin_line_setup>1:
			setup_val=io.StringIO(text).readlines()[begin_line_setup-1:end_line_setup]
		else:
			setup_val=io.StringIO(text).readlines()[begin_line_setup-2:end_line_setup]
	else:
		setup_val=None
	#print(setup_val)	

	#check chi phí hàng tháng
	begin_MONTHCOST_list=[]
	if CONTRACT_VALUE  is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in begin_MONTHCOST):
				begin_lines_MONTHCOST=int(number)
				begin_MONTHCOST_list.append(begin_lines_MONTHCOST)
	if len(begin_MONTHCOST_list)>0:
		begin_line_MONTHCOST=min(begin_MONTHCOST_list)
	else:
		begin_line_MONTHCOST=None
	end_MONTHCOST_list=[]
	if CONTRACT_VALUE  is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in end_MONTHCOST):
				end_lines_MONTHCOST=int(number)
				end_MONTHCOST_list.append(end_lines_MONTHCOST)
	if len(end_MONTHCOST_list)>0:
		end_line_MONTHCOST=min(end_MONTHCOST_list)
	else:
		end_line_MONTHCOST=None

	if end_line_MONTHCOST is not None and begin_line_MONTHCOST is not None:
		if begin_line_MONTHCOST>1:
			monthcost=io.StringIO(text).readlines()[begin_line_MONTHCOST-2:end_lines_MONTHCOST+3]
		else:
			monthcost=io.StringIO(text).readlines()[begin_line_MONTHCOST-1:end_lines_MONTHCOST+3]
	else:
		monthcost=None
	#print(monthcost)

	#check chi phí đấu nối,hòa mạng
	begin_zone_SETUP2_list=[]
	if CONTRACT_VALUE is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in begin_zone_SETUP2):
				begin_lines_setup=int(number)
				begin_zone_SETUP2_list.append(begin_lines_setup)
	if len(begin_zone_SETUP2_list)>0:
		begin_line_setup=min( begin_zone_SETUP2_list)
	else:
		begin_line_setup=None
	end_zone_SETUP2_list=[]
	if CONTRACT_VALUE  is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in end_zone_SETUP2):
				end_lines_setup=int(number)
				end_zone_SETUP2_list.append(end_lines_setup)
	if len(end_zone_SETUP2_list)>0:
		end_line_setup=min(end_zone_SETUP2_list)
	else:
		end_line_setup=None

	if end_line_setup is not None and begin_line_setup is not None:
		if begin_line_setup>1:
			setup_val2=io.StringIO(text).readlines()[begin_line_setup-2:end_line_setup+3]
		else:
			setup_val2=io.StringIO(text).readlines()[begin_line_setup-1:end_line_setup+3]
	else:
		setup_val2=None
	#print(setup_val2)
	#check Cước phí sử dụng dịch vụ
	begin_zone_SETUP3_list=[]
	if CONTRACT_VALUE is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in begin_zone_SETUP3):
				begin_lines_setup=int(number)
				begin_zone_SETUP3_list.append(begin_lines_setup)
	if len(begin_zone_SETUP3_list)>0:
		begin_line_setup=min( begin_zone_SETUP3_list)
	else:
		begin_line_setup=None
	end_zone_SETUP3_list=[]
	if CONTRACT_VALUE  is not None:
		for number,line in enumerate(text.splitlines(),1):
			if any(word in line for word in end_zone_SETUP3):
				end_lines_setup=int(number)
				end_zone_SETUP3_list.append(end_lines_setup)
	if len(end_zone_SETUP3_list)>0:
		end_line_setup=min(end_zone_SETUP3_list)
	else:
		end_line_setup=None

	if end_line_setup is not None and begin_line_setup is not None:
		if begin_line_setup>1:
			setup_val3=io.StringIO(text).readlines()[begin_line_setup-2:end_line_setup+3]
		else:
			setup_val3=io.StringIO(text).readlines()[begin_line_setup-1:end_line_setup+3]
	else:
		setup_val3=None
	#print(setup_val3)		
	

#---------------------------------------------------------------------------------
	signal_line_CONTRACT_NAME=          ['HỢP ĐỒNG']
	signal_line_TEMPLE_CODE = 			["Số:"]
	signal_line_ISSUED_DAY = 			['Hôm nay','Ngày','tháng','năm']


	signal_line_BUYER=["Người đại diện :","Người đại diện:"]
	signal_line_BUYER_ADDRESS=['Địa chỉ :']
	signal_line_BUYER_TAXCODE=['Mã số thuế :']

	signal_line_SELLER=["Người đại diện :","Người đại diện:"]
	signal_line_SELLER_ADDRESS=['Địa chỉ :']
	signal_line_SELLER_TAXCODE=['Mã số thuế:','Mã số thuế :']
	
	signal_line_preTAX_AMOUNT =			['Cộng tiền hàng (Total amount)','Cộng tiền hàng','Tiền hàng hóa, dịch vụ','Cộng tiền dịch vụ','Cộng/ Total','Tiền trước thuế (Amount before VAT)',
										'Tổng tiền (Total):','Cộng tiền hàng chưa có thuế GTGT','chưa bao gồm thuế']
	signal_line_afterTAX_AMOUNT =		['Tổng cộng tiền thanh toán (Total payment)','Tổng cộng tiền thanh toán','Tổng tiền thanh toán', 'Thành tiền/Total amount',
										'TỔNG CỘNG TIỀN THANH TOÁN','Tổng cộng tiền thanh toán  (Total of payment)','Tổng cộng tiền thanh toán:',
										'Cộng tiền thanh toán','Tiền thanh toán','Tổng số tiền thanh toán','Tổng tiền (Total Amount)','Tổng cộng tiền:','đã bao gồm thuế']

	signal_line_MONTHCOST=['Tổng giá trị thanh toán',"tiền", "Cộng", "CỘNG",'Tổng cộng',"Tiền",'Thuế']
	#PATTERN
	pattern_MONEY_DOT = 				'[\d]+[.,\d]+|[\d]*[.][\d]+|[\d]+'
	pattern_VAT = 						[0,5,10]
	#remove
	remove_preTAX_AMOUNT = 				['Tổng cộng tiền thanh toán (Total payment)','Tổng cộng tiền thanh toán','Tổng tiền thanh toán', 'Thành tiền/Total amount',
										'TỔNG CỘNG TIỀN THANH TOÁN','Tổng cộng tiền thanh toán  (Total of payment)','Tổng cộng tiền thanh toán:',
										'Cộng tiền thanh toán','Tiền thanh toán','Tổng số tiền thanh toán','Tổng tiền (Total Amount)',
										'thuê', 'Thuế','THUẾ','Tổng cộng']
#---------------------------------------------------------------------------------
	#ZONEINFO
	list_CONTRACT_NAME=[]
	if ZONE_INFO is not None:
		for line in ZONE_INFO:
			if any(word in line for word in signal_line_CONTRACT_NAME):
				#print(line)
				pre_CONTRACT_NAME=line
				#print(pre_CONTRACT_NAME)
				pre_CONTRACT_NAME=pre_CONTRACT_NAME.replace(' ', '')
				#print(pre_CONTRACT_NAME)
				pre_CONTRACT_NAME=pre_CONTRACT_NAME.replace("\n", "")
				#print(pre_CONTRACT_NAME)
				if len(pre_CONTRACT_NAME)<=50:
					CONTRACT_NAME=pre_CONTRACT_NAME
					list_CONTRACT_NAME.append(CONTRACT_NAME)
	if len(list_CONTRACT_NAME)>0:
		CONTRACT_NAME=list_CONTRACT_NAME[0]
	else:
		CONTRACT_NAME = None

	list_temple_code=[]
	if ZONE_INFO is not None:
		for line in ZONE_INFO:
			if any(word in line for word in signal_line_TEMPLE_CODE):
				#print(line)
				pre_TEMPLE_CODE=line
				#print(pre_CONTRACT_NAME)
				pre_TEMPLE_CODE=pre_TEMPLE_CODE.replace('Số:', '')
				#print(pre_TEMPLE_CODE)
				pre_TEMPLE_CODE=pre_TEMPLE_CODE.replace(' ', '')
				pre_TEMPLE_CODE=pre_TEMPLE_CODE.replace("\n", "")
				#print(pre_TEMPLE_CODE)
				if len(pre_TEMPLE_CODE)<=20:
					TEMPLE_CODE=pre_TEMPLE_CODE
					list_temple_code.append(TEMPLE_CODE)
	if len(list_temple_code)>0:
		TEMPLE_CODE=list_temple_code[0]
	else:
		TEMPLE_CODE=None
	#print("TEMPLE_CODE: "+str(pre_TEMPLE_CODE))

	#   CONTRACTORS_A
	list_buyer=[]
	if Contractors_A is not None:
		for line in Contractors_A:
			if any(word in line for word in signal_line_BUYER):
				pre_BUYER=line
				pre_BUYER=pre_BUYER.replace("Người đại diện :","")
				pre_BUYER=pre_BUYER.replace("Người đại diện:","")
				pre_BUYER=pre_BUYER.replace(' ','')
				pre_BUYER=pre_BUYER.replace("\n",'')
				#print("buyer:"+ pre_BUYER)
				if pre_BUYER!='':
					BUYER=pre_BUYER
					list_buyer.append(BUYER)
	if len(list_buyer)>0:
		BUYER=list_buyer[0]
	else:
		BUYER=None

	list_adress1=[]
	if Contractors_A is not None:
		for i in range(len(Contractors_A)):
			#print(Contractors_A[i])
			if any(word in Contractors_A[i] for word in signal_line_BUYER_ADDRESS):
				Contractors_A[i]=Contractors_A[i].replace('\n','')
				if 'Địa chỉ :' in Contractors_A[i] :
					adress=str(Contractors_A[i-1])+str(Contractors_A[i+1])
					adress=adress.replace('\n','')
					#print("BUYER ADDRESS1"+adress)
				else:
					adress=Contractors_A[i].replace('Địa chỉ :','')
					#print("BUYER ADDRESS1"+adress)
				if (re.search("Chức vụ :"or"Điện thoại :", adress) is None) and adress!="" :
					list_adress1.append(adress)
	if len(list_adress1)>0:
		adress1=list_adress1[0]
	else:
		adress1=None

	list_BUYER_TAXCODE=[]
	if Contractors_A is not None:
		for line in Contractors_A:
			if any(word in line for word in  signal_line_BUYER_TAXCODE):
				pre_BUYER_TAXCODE=line
				pre_BUYER_TAXCODE=pre_BUYER_TAXCODE.replace("Mã số thuế :","")
				pre_BUYER_TAXCODE=pre_BUYER_TAXCODE.replace("Mã số thuế:","")
				pre_BUYER_TAXCODE=pre_BUYER_TAXCODE.replace(' ','')
				pre_BUYER_TAXCODE=pre_BUYER_TAXCODE.replace("\n",'')
				#print("mst"+str(pre_BUYER_TAXCODE))
				if (re.search('[a-zA-Z]', pre_BUYER_TAXCODE) is None) and pre_BUYER_TAXCODE!='':
					BUYER_TAXCODE1=pre_BUYER_TAXCODE
					list_BUYER_TAXCODE.append(BUYER_TAXCODE1)
	if len( list_BUYER_TAXCODE)>0:
		BUYER_TAXCODE1=list_BUYER_TAXCODE[0]
	else:
		BUYER_TAXCODE1=None

	#   CONTRACTORS_B
	#print(Contractors_B)
	list_seller=[]
	if Contractors_B is not None:
		for line in Contractors_B:
			if any(word in line for word in signal_line_SELLER):
				pre_SELLER=line
				pre_SELLER=pre_SELLER.replace("Người đại diện :","")
				pre_SELLER=pre_SELLER.replace("Người đại diện:","")
				pre_SELLER=pre_SELLER.replace(' ','')
				pre_SELLER=pre_SELLER.replace("\n",'')
				#print("seller:"+ pre_SELLER)
				if pre_SELLER!='':
					SELLER=pre_SELLER
					list_seller.append(SELLER)
	if len(list_seller)>0:
		SELLER=list_seller[0]
	else:
		SELLER=None

	list_adress2=[]
	if Contractors_B is not None:
		for i in range(len(Contractors_B)):
			#print(Contractors_A[i])
			if any(word in Contractors_B[i] for word in signal_line_SELLER_ADDRESS):
				Contractors_B[i]=Contractors_B[i].replace('\n','')
				if 'Địa chỉ :' == Contractors_B[i] :
					adressB=str(Contractors_B[i-1])+str(Contractors_B[i+1])
					adressB=adress.replace('\n','')
					#print("seller ADDRESS1"+adressB)
				else:
					adressB=Contractors_B[i].replace('Địa chỉ :','')
					#print("seller ADDRESS2"+adressB)  
				if (re.search("Chức vụ :"or"Điện thoại :", adressB) is None) and adressB!="" :
					#print(adressB)
					list_adress2.append(adressB)
	if len(list_adress2)>0:
		adress2=list_adress2[0]
	else:
		adress2=None

	list_SELLER_TAXCODE=[]
	if Contractors_B is not None:
		for line in Contractors_B:
			if any(word in line for word in  signal_line_SELLER_TAXCODE):
				#print(line)
				pre_SELLER_TAXCODE=line
				pre_SELLER_TAXCODE=pre_SELLER_TAXCODE.replace("Mã số thuế :","")
				pre_SELLER_TAXCODE=pre_SELLER_TAXCODE.replace("Mã số thuế:","")
				pre_SELLER_TAXCODE=pre_SELLER_TAXCODE.replace(' ','')
				pre_SELLER_TAXCODE=pre_SELLER_TAXCODE.replace("\n",'')
				#print("mst"+str(pre_SELLER_TAXCODE))
				if (re.search('[a-zA-Z]', pre_SELLER_TAXCODE) is None) and pre_SELLER_TAXCODE!='':
					SELLER_TAXCODE1=pre_SELLER_TAXCODE
					list_SELLER_TAXCODE.append(SELLER_TAXCODE1)
	if len(list_SELLER_TAXCODE)>0:
		SELLER_TAXCODE1=list_SELLER_TAXCODE[0]
	else:
		SELLER_TAXCODE1=None
		
#---------------------------------------------------------------------------------

	pre_list_MONEY1=[]
	max_MONEY1=None
	list_MONEY1=[]

	if setup_val is not None:
		for line in setup_val:
			if "Miễn phí lắp đặt" in line:
				max_MONEY1=0
			else:
				if any(word in line for word in  signal_line_MONTHCOST):
					#print(line)
					if re.search(pattern_MONEY_DOT,line) is not None:
						for catch in re.finditer(pattern_MONEY_DOT,line):
							number=catch[0]
							res = number.strip('][').split(', ')
							remove_dot = str.maketrans('','', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>3:
								MONEY1  = (list_money_remove_dot)[0]
								pre_list_MONEY1.append(MONEY1)
					
		if len(pre_list_MONEY1)>0:
			list_MONEY1 = [money.replace("," , "") for money in pre_list_MONEY1]
			max_MONEY1 = max(list_MONEY1)
	#print(pre_list_MONEY1)
#---------------------------------------------------------
	pre_list_PRETAX_AMOUNT1 = []
	if setup_val is not None:
		for no_line, line in enumerate(setup_val):
			if any(word in line for word in signal_line_preTAX_AMOUNT):
				current_no_line = no_line 
				next_no_line = no_line + 1
				try:
					next_line_PRETAX_AMOUNT = setup_val[next_no_line]

				except Exception:
					next_line_PRETAX_AMOUNT = None	

				if re.search(pattern_MONEY_DOT, line) is not None: ##Tìm giá trị tiền trong line
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')

							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_PRETAX_AMOUNT  = (list_money_remove_dot)[0]
								pre_list_PRETAX_AMOUNT1.append(tempt_PRETAX_AMOUNT)
								#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT))

				
				#Trường hợp không tìm thấy trong hàng, thử đọc ở hàng kế tiếp
				elif (next_line_PRETAX_AMOUNT is not None) and (not any(word in next_line_PRETAX_AMOUNT for word in remove_preTAX_AMOUNT)):
						if re.search(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT) is not None:
							for catch in re.finditer(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT):
								number = (catch[0])
								#Kiểm tra số tiền nếu không có giá trị thập phân:
								if not (("." in number) and ("," in number)):
									res = number.strip('][').split(', ')
									remove_dot = str.maketrans('', '', '.')
									list_money_remove_dot = [s.translate(remove_dot) for s in res]
									if len(list_money_remove_dot[0])>2:
										tempt_PRETAX_AMOUNT  = (list_money_remove_dot)[0]
										pre_list_PRETAX_AMOUNT1.append(tempt_PRETAX_AMOUNT)
										#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT))	
	#--------------------------------------------------------------------------------
	
	pre_list_AFTERTAX_AMOUNT1 = []
	if setup_val is not None:
		for line in setup_val:
			if any(word in line for word in signal_line_afterTAX_AMOUNT):
				if re.search(pattern_MONEY_DOT, line) is not None: 
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')
							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_AFTERTAX_AMOUNT  = (list_money_remove_dot)[0]
								pre_list_AFTERTAX_AMOUNT1.append(tempt_AFTERTAX_AMOUNT)
								#print("[LOG] after_AMOUNT: " + str(tempt_AFTERTAX_AMOUNT))
	
	##Xóa dấu comma trong định dàng tiền (nếu có)
	clean_pre_list_PRETAX_AMOUNT = [money.replace(",", "") for money in pre_list_PRETAX_AMOUNT1]
	clean_pre_list_AFTERTAX_AMOUNT = [money.replace(",", "") for money in pre_list_AFTERTAX_AMOUNT1]
	#print(clean_pre_list_PRETAX_AMOUNT)
	#print(clean_pre_list_AFTERTAX_AMOUNT)

	list_VAT = []
	list_PRETAX_AMOUNT = []
	list_AFTERTAX_AMOUNT = []

	#print(len(clean_pre_list_PRETAX_AMOUNT))
	#print(len(clean_pre_list_AFTERTAX_AMOUNT))
	if  len(clean_pre_list_PRETAX_AMOUNT) == 1 and len(clean_pre_list_AFTERTAX_AMOUNT) == 1:
		pre_PRETAX_AMOUNT = int(clean_pre_list_PRETAX_AMOUNT[0])
		pre_AFTERTAX_AMOUNT = int(clean_pre_list_AFTERTAX_AMOUNT[0])
		VAT = round(((pre_AFTERTAX_AMOUNT- pre_PRETAX_AMOUNT)/pre_PRETAX_AMOUNT)*100,2)
		if VAT in pattern_VAT:#=> Kiểm tra VAT true/false?
			#print(VAT)
			PRETAX_AMOUNT = pre_PRETAX_AMOUNT
			AFTERTAX_AMOUNT = pre_AFTERTAX_AMOUNT
			list_VAT.append(VAT)
			list_PRETAX_AMOUNT.append(PRETAX_AMOUNT)
			list_AFTERTAX_AMOUNT.append(AFTERTAX_AMOUNT)
		else:
			PRETAX_AMOUNT = str(pre_PRETAX_AMOUNT)+"error"
			AFTERTAX_AMOUNT = str(pre_AFTERTAX_AMOUNT)+"error"
			list_VAT.append(VAT)
			list_PRETAX_AMOUNT.append(PRETAX_AMOUNT)
			list_AFTERTAX_AMOUNT.append(AFTERTAX_AMOUNT)			
	#print(list_PRETAX_AMOUNT)
	#print(list_AFTERTAX_AMOUNT)
	PRETAX_AMOUNT = None
	AFTERTAX_AMOUNT = None	

	if len(list_PRETAX_AMOUNT) > 0:
		PRETAX_AMOUNT = list_PRETAX_AMOUNT[0]
	

	
	if len(list_AFTERTAX_AMOUNT) > 0:
		AFTERTAX_AMOUNT = list_AFTERTAX_AMOUNT[0]

#---------------------------------------------------------------------------------------
	max_MONEY2=None
	list_MONEY2=[]
	pre_list_MONEY2=[]
	if	monthcost is not None:
		for line in monthcost:
			if any(word in line for word in  signal_line_MONTHCOST):
				if re.search(pattern_MONEY_DOT,line) is not None:
					for catch in re.finditer(pattern_MONEY_DOT,line):
						number=catch[0]
						res = number.strip('][').split(', ')
						remove_dot = str.maketrans('','', '.')
						list_money_remove_dot = [s.translate(remove_dot) for s in res]
						if len(list_money_remove_dot[0])>3:
							MONEY  = (list_money_remove_dot)[0]
							pre_list_MONEY2.append(MONEY)
	list_MONEY2 = [money.replace(",", "") for money in pre_list_MONEY2]
	if list_MONEY2 is  None:
		max_MONEY2=None
	else:  
		try:
			max_MONEY2 = max(list_MONEY2)
		except:
			max_MONEY2= None
#---------------------------------------------------------
	pre_list_PRETAX_AMOUNT2 = []
	if monthcost is not None:
		for no_line, line in enumerate(monthcost):
			if any(word in line for word in signal_line_preTAX_AMOUNT):
				current_no_line = no_line 
				next_no_line = no_line + 1
				try:
					next_line_PRETAX_AMOUNT = monthcost[next_no_line]

				except Exception:
					next_line_PRETAX_AMOUNT = None	

				if re.search(pattern_MONEY_DOT, line) is not None: ##Tìm giá trị tiền trong line
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')

							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_PRETAX_AMOUNT2  = (list_money_remove_dot)[0]
								pre_list_PRETAX_AMOUNT2.append(tempt_PRETAX_AMOUNT2)
								#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT2))

				
				#Trường hợp không tìm thấy trong hàng, thử đọc ở hàng kế tiếp
				elif (next_line_PRETAX_AMOUNT is not None) and (not any(word in next_line_PRETAX_AMOUNT for word in remove_preTAX_AMOUNT)):
						if re.search(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT) is not None:
							for catch in re.finditer(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT):
								number = (catch[0])
								#Kiểm tra số tiền nếu không có giá trị thập phân:
								if not (("." in number) and ("," in number)):
									res = number.strip('][').split(', ')
									remove_dot = str.maketrans('', '', '.')
									list_money_remove_dot = [s.translate(remove_dot) for s in res]
									if len(list_money_remove_dot[0])>2:
										tempt_PRETAX_AMOUNT2  = (list_money_remove_dot)[0]
										pre_list_PRETAX_AMOUNT2.append(tempt_PRETAX_AMOUNT2)
										#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT2))	
	#--------------------------------------------------------------------------------
	
	pre_list_AFTERTAX_AMOUNT2 = []
	if monthcost is not None:
		for line in monthcost:
			if any(word in line for word in signal_line_afterTAX_AMOUNT):
				if re.search(pattern_MONEY_DOT, line) is not None: 
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')
							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_AFTERTAX_AMOUNT2  = (list_money_remove_dot)[0]
								pre_list_AFTERTAX_AMOUNT2.append(tempt_AFTERTAX_AMOUNT2)
								#print("[LOG] after_AMOUNT: " + str(tempt_AFTERTAX_AMOUNT2))
	
	##Xóa dấu comma trong định dàng tiền (nếu có)
	clean_pre_list_PRETAX_AMOUNT2 = [money.replace(",", "") for money in pre_list_PRETAX_AMOUNT2]
	clean_pre_list_AFTERTAX_AMOUNT2 = [money.replace(",", "") for money in pre_list_AFTERTAX_AMOUNT2]

	#print(clean_pre_list_AFTERTAX_AMOUNT2)
	list_VAT2 = []
	list_PRETAX_AMOUNT2 = []
	list_AFTERTAX_AMOUNT2 = []


	if  len(clean_pre_list_PRETAX_AMOUNT2) == 1 and len(clean_pre_list_AFTERTAX_AMOUNT2) == 1:
		pre_PRETAX_AMOUNT2 = int(clean_pre_list_PRETAX_AMOUNT2[0])
		pre_AFTERTAX_AMOUNT2 = int(clean_pre_list_AFTERTAX_AMOUNT2[0])
		VAT = round(((pre_AFTERTAX_AMOUNT2- pre_PRETAX_AMOUNT2)/pre_PRETAX_AMOUNT2)*100,2)
		if VAT in pattern_VAT:#=> Kiểm tra VAT true/false?

			PRETAX_AMOUNT2 = pre_PRETAX_AMOUNT2
			AFTERTAX_AMOUNT2 = pre_AFTERTAX_AMOUNT2
			list_VAT2.append(VAT)
			list_PRETAX_AMOUNT2.append(PRETAX_AMOUNT2)
			list_AFTERTAX_AMOUNT2.append(AFTERTAX_AMOUNT2)
			#print(list_AFTERTAX_AMOUNT2)

	PRETAX_AMOUNT2 = None
	AFTERTAX_AMOUNT2 = None	

	if len(list_PRETAX_AMOUNT2) > 0:
		PRETAX_AMOUNT2 = list_PRETAX_AMOUNT2[0]
	
	if len(list_AFTERTAX_AMOUNT2) > 0:
		AFTERTAX_AMOUNT2 = list_AFTERTAX_AMOUNT2[0]
#------------------------------------------------------------------------------------------------
	#---------------------------------------------------------------------------------------
	max_MONEY3=None
	list_MONEY3=[]
	pre_list_MONEY3=[]
	if	setup_val2 is not None:
		for line in setup_val2:
			if any(word in line for word in  signal_line_MONTHCOST):
				if re.search(pattern_MONEY_DOT,line) is not None:
					for catch in re.finditer(pattern_MONEY_DOT,line):
						number=catch[0]
						res = number.strip('][').split(', ')
						remove_dot = str.maketrans('','', '.')
						list_money_remove_dot = [s.translate(remove_dot) for s in res]
						if len(list_money_remove_dot[0])>3:
							MONEY  = (list_money_remove_dot)[0]
							pre_list_MONEY3.append(MONEY)
	list_MONEY3 = [money.replace(",", "") for money in pre_list_MONEY3]
	if list_MONEY2 is  None:
		max_MONEY3=None
	else:  
		try:
			max_MONEY3 = max(list_MONEY3)
		except:
			max_MONEY3= None
#---------------------------------------------------------
	pre_list_PRETAX_AMOUNT3 = []
	if setup_val2 is not None:
		for no_line, line in enumerate(setup_val2):
			if any(word in line for word in signal_line_preTAX_AMOUNT):
				current_no_line = no_line 
				next_no_line = no_line + 1
				try:
					next_line_PRETAX_AMOUNT = setup_val2[next_no_line]

				except Exception:
					next_line_PRETAX_AMOUNT = None	

				if re.search(pattern_MONEY_DOT, line) is not None: ##Tìm giá trị tiền trong line
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')

							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_PRETAX_AMOUNT3  = (list_money_remove_dot)[0]
								pre_list_PRETAX_AMOUNT3.append(tempt_PRETAX_AMOUNT3)
								#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT2))

				
				#Trường hợp không tìm thấy trong hàng, thử đọc ở hàng kế tiếp
				elif (next_line_PRETAX_AMOUNT is not None) and (not any(word in next_line_PRETAX_AMOUNT for word in remove_preTAX_AMOUNT)):
						if re.search(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT) is not None:
							for catch in re.finditer(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT):
								number = (catch[0])
								#Kiểm tra số tiền nếu không có giá trị thập phân:
								if not (("." in number) and ("," in number)):
									res = number.strip('][').split(', ')
									remove_dot = str.maketrans('', '', '.')
									list_money_remove_dot = [s.translate(remove_dot) for s in res]
									if len(list_money_remove_dot[0])>2:
										tempt_PRETAX_AMOUNT3  = (list_money_remove_dot)[0]
										pre_list_PRETAX_AMOUNT3.append(tempt_PRETAX_AMOUNT3)
										#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT2))	
	#--------------------------------------------------------------------------------
	
	pre_list_AFTERTAX_AMOUNT3 = []
	if setup_val2 is not None:
		for line in setup_val2:
			if any(word in line for word in signal_line_afterTAX_AMOUNT):
				if re.search(pattern_MONEY_DOT, line) is not None: 
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')
							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_AFTERTAX_AMOUNT3  = (list_money_remove_dot)[0]
								pre_list_AFTERTAX_AMOUNT3.append(tempt_AFTERTAX_AMOUNT3)
								#print("[LOG] after_AMOUNT: " + str(tempt_AFTERTAX_AMOUNT3))
	
	##Xóa dấu comma trong định dàng tiền (nếu có)
	clean_pre_list_PRETAX_AMOUNT3 = [money.replace(",", "") for money in pre_list_PRETAX_AMOUNT3]
	clean_pre_list_AFTERTAX_AMOUNT3 = [money.replace(",", "") for money in pre_list_AFTERTAX_AMOUNT3]

	#print(clean_pre_list_AFTERTAX_AMOUNT2)
	list_VAT3 = []
	list_PRETAX_AMOUNT3 = []
	list_AFTERTAX_AMOUNT3 = []


	if  len(clean_pre_list_PRETAX_AMOUNT3) == 1 and len(clean_pre_list_AFTERTAX_AMOUNT3) == 1:
		pre_PRETAX_AMOUNT3 = int(clean_pre_list_PRETAX_AMOUNT3[0])
		pre_AFTERTAX_AMOUNT3 = int(clean_pre_list_AFTERTAX_AMOUNT3[0])
		VAT = round(((pre_AFTERTAX_AMOUNT3- pre_PRETAX_AMOUNT3)/pre_PRETAX_AMOUNT3)*100,2)
		if VAT in pattern_VAT:#=> Kiểm tra VAT true/false?

			PRETAX_AMOUNT3 = pre_PRETAX_AMOUNT3
			AFTERTAX_AMOUNT3 = pre_AFTERTAX_AMOUNT3
			list_VAT3.append(VAT)
			list_PRETAX_AMOUNT3.append(PRETAX_AMOUNT3)
			list_AFTERTAX_AMOUNT3.append(AFTERTAX_AMOUNT3)
			#print(list_AFTERTAX_AMOUNT3)

	PRETAX_AMOUNT3 = None
	AFTERTAX_AMOUNT3 = None	

	if len(list_PRETAX_AMOUNT3) > 0:
		PRETAX_AMOUNT3 = list_PRETAX_AMOUNT3[0]
	
	if len(list_AFTERTAX_AMOUNT3) > 0:
		AFTERTAX_AMOUNT3 = list_AFTERTAX_AMOUNT3[0]
#---------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------
	max_MONEY4=None
	list_MONEY4=[]
	pre_list_MONEY4=[]
	if	setup_val3 is not None:
		for line in setup_val3:
			if any(word in line for word in  signal_line_MONTHCOST):
				if re.search(pattern_MONEY_DOT,line) is not None:
					for catch in re.finditer(pattern_MONEY_DOT,line):
						number=catch[0]
						res = number.strip('][').split(', ')
						remove_dot = str.maketrans('','', '.')
						list_money_remove_dot = [s.translate(remove_dot) for s in res]
						if len(list_money_remove_dot[0])>3:
							MONEY  = (list_money_remove_dot)[0]
							pre_list_MONEY4.append(MONEY)
	list_MONEY4 = [money.replace(",", "") for money in pre_list_MONEY4]
	if list_MONEY4 is  None:
		max_MONEY4=None
	else:  
		try:
			max_MONEY4 = max(list_MONEY4)
		except:
			max_MONEY4= None
#---------------------------------------------------------
	pre_list_PRETAX_AMOUNT4 = []
	if setup_val3 is not None:
		for no_line, line in enumerate(setup_val3):
			if any(word in line for word in signal_line_preTAX_AMOUNT):
				current_no_line = no_line 
				next_no_line = no_line + 1
				try:
					next_line_PRETAX_AMOUNT = setup_val3[next_no_line]

				except Exception:
					next_line_PRETAX_AMOUNT = None	

				if re.search(pattern_MONEY_DOT, line) is not None: ##Tìm giá trị tiền trong line
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')

							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_PRETAX_AMOUNT4  = (list_money_remove_dot)[0]
								pre_list_PRETAX_AMOUNT4.append(tempt_PRETAX_AMOUNT4)
								#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT2))

				
				#Trường hợp không tìm thấy trong hàng, thử đọc ở hàng kế tiếp
				elif (next_line_PRETAX_AMOUNT is not None) and (not any(word in next_line_PRETAX_AMOUNT for word in remove_preTAX_AMOUNT)):
						if re.search(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT) is not None:
							for catch in re.finditer(pattern_MONEY_DOT, next_line_PRETAX_AMOUNT):
								number = (catch[0])
								#Kiểm tra số tiền nếu không có giá trị thập phân:
								if not (("." in number) and ("," in number)):
									res = number.strip('][').split(', ')
									remove_dot = str.maketrans('', '', '.')
									list_money_remove_dot = [s.translate(remove_dot) for s in res]
									if len(list_money_remove_dot[0])>2:
										tempt_PRETAX_AMOUNT4  = (list_money_remove_dot)[0]
										pre_list_PRETAX_AMOUNT4.append(tempt_PRETAX_AMOUNT4)
										#print("[LOG] PRETAX_AMOUNT: " + str(tempt_PRETAX_AMOUNT2))	
	#--------------------------------------------------------------------------------
	
	pre_list_AFTERTAX_AMOUNT4 = []
	if setup_val3 is not None:
		for line in setup_val3:
			if any(word in line for word in signal_line_afterTAX_AMOUNT):
				if re.search(pattern_MONEY_DOT, line) is not None: 
					for catch in re.finditer(pattern_MONEY_DOT, line):
						number = (catch[0])
						#Kiểm tra số tiền nếu không có giá trị thập phân:
						if not (("." in number) and ("," in number)):
							res = number.strip('][').split(', ')
							remove_dot = str.maketrans('', '', '.')
							list_money_remove_dot = [s.translate(remove_dot) for s in res]
							if len(list_money_remove_dot[0])>2:
								tempt_AFTERTAX_AMOUNT4  = (list_money_remove_dot)[0]
								pre_list_AFTERTAX_AMOUNT4.append(tempt_AFTERTAX_AMOUNT4)
								#print("[LOG] after_AMOUNT: " + str(tempt_AFTERTAX_AMOUNT2))
	
	##Xóa dấu comma trong định dàng tiền (nếu có)
	clean_pre_list_PRETAX_AMOUNT4 = [money.replace(",", "") for money in pre_list_PRETAX_AMOUNT4]
	clean_pre_list_AFTERTAX_AMOUNT4 = [money.replace(",", "") for money in pre_list_AFTERTAX_AMOUNT4]

	#print(clean_pre_list_AFTERTAX_AMOUNT2)
	list_VAT4 = []
	list_PRETAX_AMOUNT4 = []
	list_AFTERTAX_AMOUNT4 = []


	if  len(clean_pre_list_PRETAX_AMOUNT4) == 1 and len(clean_pre_list_AFTERTAX_AMOUNT4) == 1:
		pre_PRETAX_AMOUNT4 = int(clean_pre_list_PRETAX_AMOUNT4[0])
		pre_AFTERTAX_AMOUNT4 = int(clean_pre_list_AFTERTAX_AMOUNT4[0])
		VAT = round(((pre_AFTERTAX_AMOUNT4- pre_PRETAX_AMOUNT4)/pre_PRETAX_AMOUNT4)*100,2)
		if VAT in pattern_VAT:#=> Kiểm tra VAT true/false?

			PRETAX_AMOUNT4 = pre_PRETAX_AMOUNT4
			AFTERTAX_AMOUNT4 = pre_AFTERTAX_AMOUNT4
			list_VAT4.append(VAT)
			list_PRETAX_AMOUNT4.append(PRETAX_AMOUNT4)
			list_AFTERTAX_AMOUNT4.append(AFTERTAX_AMOUNT4)
			#print(list_AFTERTAX_AMOUNT2)

	PRETAX_AMOUNT4 = None
	AFTERTAX_AMOUNT4 = None	

	if len(list_PRETAX_AMOUNT4) > 0:
		PRETAX_AMOUNT4 = list_PRETAX_AMOUNT4[0]
	
	if len(list_AFTERTAX_AMOUNT4) > 0:
		AFTERTAX_AMOUNT4 = list_AFTERTAX_AMOUNT4[0]
	
	
	

#--------------------------------------------------------------------------


	CUOC_PHI_SU_DUNG_DICH_VU	={"CUOC_PHI_SU_DUNG_DICH_VU":{"PRETAX_AMOUNT":PRETAX_AMOUNT4,"AFTERTAX_AMOUNT":AFTERTAX_AMOUNT4}}
	CHI_PHI_DAU_NOI_HOA_MANG	={"CHI_PHI_DAU_NOI_HOA_MANG":{"PRETAX_AMOUNT":PRETAX_AMOUNT3,"AFTERTAX_AMOUNT":AFTERTAX_AMOUNT3}}
	CHI_PHI_HANG_THANG			={"CHI_PHI_HANG_THANG":{"PRETAX_AMOUNT":PRETAX_AMOUNT2,"AFTERTAX_AMOUNT":AFTERTAX_AMOUNT2}}
	CHI_PHI_LAP_DAT				={"CHI_PHI_LAP_DAT":{"PRETAX_AMOUNT":PRETAX_AMOUNT,"AFTERTAX_AMOUNT":AFTERTAX_AMOUNT}}
	#result
	FILL_RESULT = 	{"CONTRACT":{"CONTRACT_NAME":CONTRACT_NAME,"TEMPLE_CODE":TEMPLE_CODE},
					"BEN_A":{"BUYER":BUYER,"DIA_CHI":adress1, "TAX_CODE":BUYER_TAXCODE1},
					"BEN_B":{"SELLER":SELLER,"DIA_CHI":adress2,"TAX_CODE":SELLER_TAXCODE1}
					}
	#FILL_RESULT.update(CHI_PHI_DAU_NOI_HOA_MANG)
	#FILL_RESULT.update(CUOC_PHI_SU_DUNG_DICH_VU)
	if	(PRETAX_AMOUNT is not None) or (AFTERTAX_AMOUNT is not None):
		if list_content != []:
			danhmuc={"DANH_MUC":list_content[0]}
			CHI_PHI_LAP_DAT["CHI_PHI_LAP_DAT"].update(danhmuc)
		FILL_RESULT.update(CHI_PHI_LAP_DAT)
	if	(PRETAX_AMOUNT2 is not None) or (AFTERTAX_AMOUNT2 is not None):
		if list_content != []:
			danhmuc={"DANH_MUC":list_content[1]}
			CHI_PHI_HANG_THANG["CHI_PHI_HANG_THANG"].update(danhmuc)	
		FILL_RESULT.update(CHI_PHI_HANG_THANG)
	if	(PRETAX_AMOUNT3 is not None) or (AFTERTAX_AMOUNT3 is not None):
		if list_content != []:
			danhmuc={"DANH_MUC":list_content[0]}
			CHI_PHI_DAU_NOI_HOA_MANG["CHI_PHI_DAU_NOI_HOA_MANG"].update(danhmuc)		
		FILL_RESULT.update(CHI_PHI_DAU_NOI_HOA_MANG)
	if	(PRETAX_AMOUNT3 is not None) or (AFTERTAX_AMOUNT3 is not None):
		if list_content != []:
			danhmuc={"DANH_MUC":list_content[1]}
			CUOC_PHI_SU_DUNG_DICH_VU["CUOC_PHI_SU_DUNG_DICH_VU"].update(danhmuc)
		FILL_RESULT.update(CUOC_PHI_SU_DUNG_DICH_VU)
	return FILL_RESULT




				






	
