# -*- coding: utf-8 -*-
"""Briefing Report.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GQb3UROn1ZYdi3TRL0CoV7tgJ0E_Ip9t
"""

import pandas as pd
#from google.colab import files
from docxtpl import DocxTemplate, InlineImage
import numpy as np
#uploaded = files.upload()
import os
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import docx2pdf

#creates the widget
root = tk.Tk()

#sets the window title
root.title("Briefing Report Cleaner")

#set the window size
root.geometry("300x100")

#define function to open file dialog and return file path
def get_file_path():
    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx"), ("CSV Files", "*.csv")])
    return file_path

#create button to select Excel file
#select_file_button = tk.Button(root, text="Select Excel File", command=get_file_path)
#select_file_button.pack(pady=10)

#define function for cleaning (original file)

def clean_briefing_data():
    file_path = get_file_path()
    if file_path.endswith('.xlsx'):
        briefing_df = pd.read_excel(file_path)
    elif file_path.endswith('.csv'):
        briefing_df = pd.read_csv(file_path)

    briefing_df = briefing_df[briefing_df["Company Name"] != 'Ace Infoway Pvt. Ltd.'] #testing this line to remove ace
    briefing_df = briefing_df.drop(columns=['IP Address', 'Demo', 'Comp'])
    briefing_df = briefing_df[briefing_df['Page Name'].str.contains('Briefing')]
    briefing_df['Created'] = pd.to_datetime(briefing_df['Created'])

    total = briefing_df['User Name'].count()
    month = briefing_df['Created'].dt.strftime('%B').values[0]

    #Counting all of the briefings that were accessed, then ordering by counts, dropping extra columns and rows 
    briefing_counts = briefing_df.groupby(['Action URL']).count().reset_index()
    briefing_counts = briefing_counts.sort_values(by=["User Name"], ascending=False)
    briefing_counts = briefing_counts[briefing_counts["Action URL"] != "/login"]
    briefing_counts = briefing_counts[briefing_counts["Action URL"] != "/View/BriefingServices"]
    briefing_counts = briefing_counts.drop(columns=['User Name', 'Page Name', 'Action Name', 'Created'])
    briefing_counts = briefing_counts.rename(columns={'Action URL': 'Briefing Title', 'Company Name': 'Count'})
    most_active_briefings = briefing_counts.head(5)


    #internal only
    
    internal = briefing_df[briefing_df['Company Name'].str.contains('Inteserra', na=False)]
    internal_p = briefing_df[briefing_df['Company Name'].str.contains('Inteserra', na=False)]
    internal = internal.groupby(['Action URL']).count().reset_index()
    internal = internal.sort_values(by=["User Name"], ascending=False)
    internal = internal[internal["Action URL"] != "/login"]
    internal = internal[internal["Action URL"] != "/View/BriefingServices"]
    internal = internal.drop(columns=['User Name', 'Page Name', 'Action Name', 'Created'])
    internal = internal.rename(columns={'Action URL': 'Briefing Title', 'Company Name': 'Count'})
    internal_most_active_briefings = internal.head(5)

    #take counts of briefings view/downloaded by company
    company_counts = briefing_df[briefing_df["Action URL"] != "/login"]
    company_counts = company_counts[company_counts["Action URL"] != "/View/BriefingServices"]
    company_counts = company_counts.groupby(['Company Name']).count().reset_index()
    company_counts = company_counts.sort_values(by=["User Name"], ascending=False)
    company_counts = company_counts[company_counts["Company Name"] != "Inteserra"]
    company_counts = company_counts.drop(columns=['Action URL', 'Page Name', 'Action Name', 'Created'])
    company_counts = company_counts.rename(columns={'Action URL': 'Company Name', 'User Name': 'Count'})
    most_active_companies = company_counts.head(5)


    #broken down by user & company
    user_counts = briefing_df[briefing_df["Action URL"] != "/login"]
    user_counts = user_counts[user_counts["Action URL"] != "/View/BriefingServices"]
    user_counts = user_counts[user_counts["Company Name"] != "Inteserra"]
    user_counts = user_counts.sort_values(['Company Name', 'User Name'])
    user_counts = user_counts.groupby(["Company Name", "User Name"]).count()
    user_counts = user_counts.sort_values(by=["Page Name"], ascending=False)
    user_counts = user_counts.drop(columns=['Action URL', 'Action Name', 'Created'])
    user_counts = user_counts.rename(columns={'Page Name': 'Count'})
    most_active_users = user_counts.head(5)


    #next calculate the total # of briefings downloaded/viewed (do we already have that on KPI report colab??), we do, split between int/ext, and how many are solutions members, sales members, etc. 
    #then finally access denied data, which we already have
    briefing_total = briefing_df[briefing_df['Page Name'].str.contains('Briefing')]
    inteserra =('Inteserra', 'FAStek Compliance Solutions, Inc.', 'Lance J.M. Steinhart, P.C.')

    # internal count
    briefing_int = briefing_total[briefing_total['Company Name'].isin(inteserra)]
    abcd = briefing_int.count()

    # external count
    briefing_ext = briefing_total[~briefing_total['Company Name'].isin(inteserra)]
    efg = briefing_ext.count()

    solutions = ('Peter Nielsen', 'Ann Marie Kemp', 'Christina Ward', 'Scott Klopack')
    sales = ('Michael Yokay', 'Lindsay Swany')

    #solutions count
    solutions_count = briefing_int[briefing_int['User Name'].isin(solutions)].count()


    #sales count
    sales_count = briefing_int[briefing_int['User Name'].isin(sales)].count()

    denied_df = briefing_df[briefing_df["Action URL"].str.contains("Denied", na=False)]
    denied_df = denied_df.groupby(["Company Name", "User Name"]).count()
    denied_df = denied_df.sort_values(by=["Page Name"], ascending=False)

    denied_df = denied_df.drop(columns=['Action URL', 'Action Name', 'Created'])
    denied_df = denied_df.rename(columns={'Page Name': 'Count'})


    #load the word template
    doc = DocxTemplate("template.docx")


    # Define the context for the template
    #most_active_briefings
    most_active_briefing1_name = most_active_briefings.iloc[0]['Briefing Title']
    most_active_briefing2_name = most_active_briefings.iloc[1]['Briefing Title']
    most_active_briefing3_name = most_active_briefings.iloc[2]['Briefing Title']
    most_active_briefing4_name = most_active_briefings.iloc[3]['Briefing Title']
    most_active_briefing5_name = most_active_briefings.iloc[4]['Briefing Title']

    most_active_briefing1_count = most_active_briefings.iloc[0]['Count']
    most_active_briefing2_count = most_active_briefings.iloc[1]['Count']
    most_active_briefing3_count = most_active_briefings.iloc[2]['Count']
    most_active_briefing4_count = most_active_briefings.iloc[3]['Count']
    most_active_briefing5_count = most_active_briefings.iloc[4]['Count']

    #internal most active briefings
    int_most_active_brief1_name = internal_most_active_briefings.iloc[0]['Briefing Title']
    int_most_active_brief2_name = internal_most_active_briefings.iloc[1]['Briefing Title']
    int_most_active_brief3_name = internal_most_active_briefings.iloc[2]['Briefing Title']
    int_most_active_brief4_name = internal_most_active_briefings.iloc[3]['Briefing Title']
    int_most_active_brief5_name = internal_most_active_briefings.iloc[4]['Briefing Title']

    int_most_active_brief1_count = internal_most_active_briefings.iloc[0]['Count']
    int_most_active_brief2_count = internal_most_active_briefings.iloc[1]['Count']
    int_most_active_brief3_count = internal_most_active_briefings.iloc[2]['Count']
    int_most_active_brief4_count = internal_most_active_briefings.iloc[3]['Count']
    int_most_active_brief5_count = internal_most_active_briefings.iloc[4]['Count']

    #most_active_companies
    most_active_company1_name = most_active_companies.iloc[0]['Company Name']
    most_active_company2_name = most_active_companies.iloc[1]['Company Name']
    most_active_company3_name = most_active_companies.iloc[2]['Company Name']
    most_active_company4_name = most_active_companies.iloc[3]['Company Name']
    most_active_company5_name = most_active_companies.iloc[4]['Company Name']

    most_active_company1_count = most_active_companies.iloc[0]['Count']
    most_active_company2_count = most_active_companies.iloc[1]['Count']
    most_active_company3_count = most_active_companies.iloc[2]['Count']
    most_active_company4_count = most_active_companies.iloc[3]['Count']
    most_active_company5_count = most_active_companies.iloc[4]['Count']

    #most active users
    alpha = most_active_users.reset_index()

    active_user_company1 = alpha.iloc[0]['Company Name']
    active_user_company2 = alpha.iloc[1]['Company Name']
    active_user_company3 = alpha.iloc[2]['Company Name']
    active_user_company4 = alpha.iloc[3]['Company Name']
    active_user_company5 = alpha.iloc[4]['Company Name']

    active_user1 = alpha.iloc[0]['User Name']
    active_user2 = alpha.iloc[1]['User Name']
    active_user3 = alpha.iloc[2]['User Name']
    active_user4 = alpha.iloc[3]['User Name']
    active_user5 = alpha.iloc[4]['User Name']

    active_user_count1 = alpha.iloc[0]['Count']
    active_user_count2 = alpha.iloc[1]['Count']
    active_user_count3 = alpha.iloc[2]['Count']
    active_user_count4 = alpha.iloc[3]['Count']
    active_user_count5 = alpha.iloc[4]['Count']

    #total briefings downloaded/viewed, broken down by subscribers, internal, sales, and solutions
    subscriber_total = efg.values[0]
    internal_total = abcd.values[0]
    solutions_total = solutions_count.values[0]
    sales_total = sales_count.values[0]




    n = 5 
    top_companies = company_counts["Company Name"][:n].tolist()
    other_companies = company_counts["Count"][n:].sum()
    top_c_counts = company_counts["Count"][:n].tolist()
    top_c_counts.append(other_companies)
    top_companies.append('Others')

    colors = ['#BF29FF', '#2D0080', '#0E1D66', '#261342', '#36454F', '#1C1854']

    fig, ax = plt.subplots()
    ax.pie(top_c_counts, colors=colors, labels=top_companies, autopct='%1.1f%%', textprops={'color': 'grey'})
    ax.set_title('Most Active Companies - Briefings')

    plt.savefig('briefingpiechart.png', bbox_inches='tight')

    image = InlineImage(doc, 'briefingpiechart.png', height=2500000)
#---------------------------------------------------------------------------------------#







#these are the key value pairs that allow us to import to the template document
    context = {"MONTH": month,
            "TOTAL": total,
            "BRIEFING1": most_active_briefing1_name,
            "BRIEFING2": most_active_briefing2_name,
            "BRIEFING3": most_active_briefing3_name,
            "BRIEFING4": most_active_briefing4_name,
            "BRIEFING5": most_active_briefing5_name,
            "BRIEFCOUNT1": most_active_briefing1_count,
            "BRIEFCOUNT2": most_active_briefing2_count,
            "BRIEFCOUNT3": most_active_briefing3_count,
            "BRIEFCOUNT4": most_active_briefing4_count,
            "BRIEFCOUNT5": most_active_briefing5_count,
            "INTBRIEF1": int_most_active_brief1_name,
            "INTBRIEF2": int_most_active_brief2_name,
            "INTBRIEF3": int_most_active_brief3_name,
            "INTBRIEF4": int_most_active_brief4_name,
            "INTBRIEF5": int_most_active_brief5_name,
            "INTCOUNT1": int_most_active_brief1_count,
            "INTCOUNT2": int_most_active_brief2_count,
            "INTCOUNT3": int_most_active_brief3_count,
            "INTCOUNT4": int_most_active_brief4_count,
            "INTCOUNT5": int_most_active_brief5_count,
            "COMPANY1": most_active_company1_name,
            "COMPANY2": most_active_company2_name,
            "COMPANY3": most_active_company3_name,
            "COMPANY4": most_active_company4_name,
            "COMPANY5": most_active_company5_name,
            "COMPANY1COUNT": most_active_company1_count,
            "COMPANY2COUNT": most_active_company2_count,
            "COMPANY3COUNT": most_active_company3_count,
            "COMPANY4COUNT": most_active_company4_count,
            "COMPANY5COUNT": most_active_company5_count,
            "ACTUSERSCO1": active_user_company1,
            "ACTUSERSCO2": active_user_company2,
            "ACTUSERSCO3": active_user_company3,
            "ACTUSERSCO4": active_user_company4,
            "ACTUSERSCO5": active_user_company5,
            "ACTUSER1": active_user1,
            "ACTUSER2": active_user2,
            "ACTUSER3": active_user3,
            "ACTUSER4": active_user4,
            "ACTUSER5": active_user5,
            "ACTUSERCOUNT1": active_user_count1,
            "ACTUSERCOUNT2": active_user_count2,
            "ACTUSERCOUNT3": active_user_count3,
            "ACTUSERCOUNT4": active_user_count4,
            "ACTUSERCOUNT5": active_user_count5,
            "SUBSCRIBER": subscriber_total,
            "INTERNAL": internal_total,
            "SALES": sales_total,
            "SOLUTIONS": solutions_total,
            "CHART": image}

    # Render the template with the context
    doc.render(context)

    # Save the output document to user's downloads
    downloads = os.path.join(os.path.expanduser("~"), "Downloads")
    output_file_path = os.path.join(downloads, "output.docx")
    doc.save(output_file_path)

    pdf_file_path = os.path.join(downloads, "output.pdf")#r
    docx2pdf.convert(output_file_path, pdf_file_path)#r

    return output_file_path, pdf_file_path #r
#create button to clean the file
clean_file_button = tk.Button(root, text = "Clean Briefing Report", command=clean_briefing_data)
clean_file_button.pack(pady=10)


root.mainloop()
#export csv of Access Denieds