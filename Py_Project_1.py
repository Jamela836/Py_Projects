#بسم الله الرحمن الرحيم

#Importing libraries
import pandas as pd
import numpy as np
import tabulate as tab
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib import font_manager

#Reading data that saved as csv file
my_data=pd.read_csv("C:\\Users\\laptop\\Desktop\\learning_python\\python_project1\\row_data.csv")

#Showing data
#print(my_data)

#Converting data into data frame format --> this necessary for cleaning steps if needed, like converting data types
data_frame=pd.DataFrame(my_data)
#Rename order date and total sales columns
data_frame=data_frame.rename(columns={'Order date ':'Order date','total sales':'Total sales'})

#Showing data frame
#print(tab.tabulate(data_frame,headers='keys',tablefmt='psql'))

#Converting order date column format from string to datetime using to_datetime
#Datetimeindex function is necessary to get year, day or month
data_frame['Order date']=pd.DatetimeIndex(pd.to_datetime(data_frame['Order date'],format='%m/%d/%Y'))

#Showing data frame after converting order date from string to datetime
#print(tab.tabulate(data_frame,headers='keys',tablefmt='psql'))

#Converting data frame into structured Numpy array, so we can use numpy functions to get insights from the data

#First we need to specify names and datatypes of columns, we can use dtype function to do this
data_type=np.dtype([
    ('Reciept no','int64'),
    ('Order date','<datetime64[D]'),
    ('Ordertype name','U20'),
    ('Item name','U20'),
    ('Category name','U20'),
    ('Selling price','float64'),
    ('Item quantity','int64'),
    ('Total sales','float64')
    ])
#Converting data frame into data array
data_array=np.array(data_frame.to_records(index=False), dtype=data_type)

#Showing the array
#print(tab.tabulate(data_array,headers='keys',tablefmt='psql'))

#Insights

#1_Total sales
total_sales=np.sum(data_array['Total sales'])
#print(total_sales)

#2_Total quantity
total_quantity=np.sum(data_array['Item quantity'])
#print(total_quantity)

#3_Calculate total sales for each category

#First we need to extract category names and total sales
category_name=data_array['Category name']
total_sales=data_array['Total sales']

#Creating two lists to get category names and total sales
categories_names_list=[]
categories_sales_list=[]
for name in np.unique(data_array['Category name']):
    each_category_sales=total_sales[category_name==name].sum()
    categories_names_list.append(name)
    categories_sales_list.append(each_category_sales)
#print(categories_names_list,categories_sales_list)

#Sorting data
categories_sorted_data=sorted(zip(categories_sales_list,categories_names_list),reverse=True)
sorted_sales,sorted_categories=zip(*categories_sorted_data)

#4_Calculate total sales for each order type

#First extract order type
order_type=data_frame['Ordertype name']

#Creating two lists for orders types names and total sales
orders_types_list=[]
orders_sales_list=[]
for type_ in np.unique(data_array['Ordertype name']):
    each_type_sales=total_sales[order_type==type_].sum()
    orders_types_list.append(type_)
    orders_sales_list.append(each_type_sales)
#print(orders_types_list,orders_sales_list)

#5_Calculate total sales for each item
#First extract item name
item_name=data_frame['Item name']

#Creating two lists for item names and total sales
items_names_list=[]
items_sales_list=[]
for item in np.unique(data_array['Item name']):
    each_item_sales=total_sales[item_name==item].sum()
    items_names_list.append(item)
    items_sales_list.append(each_item_sales)
#print(items_names_list,items_sales_list)

#6_calculate total sales for each year
order_date=data_frame['Order date']
total_sales2=data_frame['Total sales']
years=[]
years_sales=[]
for year in np.unique(order_date.dt.year):
    each_year_sales=total_sales2[order_date.dt.year==year].sum()
    years.append(year)
    years_sales.append(each_year_sales)
years_int = [int(year) for year in years]
#Sorting data
years_sorted_data=sorted(zip(years,years_sales),reverse=True)
sortedy_sales,sorted_years=zip(*years_sorted_data)
#print(years_int,years_sales)

#Visualization

#First set times new roman as the default font

#find the path of times new roman
for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'Times' in font:
        print(font)

# Save the path in a variable then extract font and save it in another one
times_new_roman_path = 'C:\\Windows\\Fonts\\times.ttf'
times_new_roman_font = font_manager.FontProperties(fname=times_new_roman_path)

# Set the font globally
rcParams['font.family'] = times_new_roman_font.get_name()

#Creating a figure to hold all charts
fig,axes=plt.subplots(2,2,figsize=(8,6),facecolor='#89A8B2')
fig.suptitle('Overall Sales Data', fontsize=48, fontweight='bold',color='#22177A')

#Chart1
axes[0,0].bar(sorted_categories,sorted_sales,width=0.5,color='#22177A')
axes[0,0].set_title('Total Sales by Category Type',fontweight='bold', color='#22177A')
axes[0,0].set_yticks(range(10000,700000,70000))
axes[0,0].tick_params(axis='x', labelcolor='#22177A', labelsize=10)
axes[0,0].tick_params(axis='y', labelcolor='#22177A', labelsize=10)
axes[0,0].spines['top'].set_visible(False)
axes[0,0].spines['right'].set_visible(False)

#chart2
axes[0,1].plot(orders_types_list,orders_sales_list,linewidth=2)
axes[0, 1].tick_params(axis='x',labelcolor='#22177A', labelsize=10)
axes[0, 1].tick_params(axis='y',labelcolor='#22177A', labelsize=10)
axes[0,1].set_title('Total Sales by Item Name',fontweight='bold', color='#22177A')
axes[0,1].spines['top'].set_visible(False)
axes[0,1].spines['right'].set_visible(False)

#chart3
axes[1,0].plot(items_names_list,items_sales_list,linewidth=2)
axes[1, 0].tick_params(axis='x', rotation=45,labelcolor='#22177A', labelsize=10)
axes[1, 0].tick_params(axis='y',labelcolor='#22177A', labelsize=10)
axes[1,0].set_title('Total Sales by Item Name',fontweight='bold', color='#22177A')
axes[1,0].spines['top'].set_visible(False)
axes[1,0].spines['right'].set_visible(False)

#chart4
axes[1,1].bar(years,years_sales,width=0.5,color='#22177A')
axes[1,1].set_xticks(years)
axes[1,1].set_title('Total Sales by Year',fontweight='bold', color='#22177A')
axes[1,1].tick_params(axis='x', labelcolor='#22177A', labelsize=10)
axes[1,1].tick_params(axis='y', labelcolor='#22177A', labelsize=10)
axes[1,1].spines['top'].set_visible(False)
axes[1,1].spines['right'].set_visible(False)

#Customize background for all charts
for ax in axes.flatten():
    ax.set_facecolor('#E5E1DA')
    ax.grid(True)
#Showing result
plt.tight_layout()
plt.show()