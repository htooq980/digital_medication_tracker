import streamlit as st
import pandas as pd
import os 
from datetime import date
import seaborn as sns
import matplotlib.pyplot as plt




if 'medications' not in st.session_state:

    if os.path.exists('medications.csv'):
        st.session_state['medications'] = pd.read_csv('medications.csv')  

    else:
        st.session_state['medications'] = pd.DataFrame()

st.title('Medication Tracker')

with st.sidebar:
    page = st.radio(
        "Main Menu",
        ['Add Medication', 'Interaction Check', 'Daily Schedule', 'Inventory','Dashboard']
    )

if page == 'Add Medication':
    st.header("Add Medication")

    med_name = st.text_input('Medicine Name')
    
    active_ingr = st.text_input('Active Ingredients')

    dosage = st.selectbox(
    "How many times do you take this medication?",
    (   "---Select---", 
        "Once a day", 
         "Twice a day", 
         "3 times a day", 
         "Every 8 hours", 
         "Once a week")
    )

    instructions = st.selectbox(
    "Instructions",
    (   "---Select---",
        "Before meals",
        "After meals",
        "On an empty stomach",
        "While eating",
        "Avoid taking it with certain food",
        "Others")
    )
    
    
    if instructions == "Others":
            
            instructions = st.text_input("Please specify")
        

    
    urge_lvl = st.selectbox(
    "Urgency level",
    ("---Select---","High", "Medium", "Low"),
    )
    


    med_category = st.selectbox(

        'Medication Category',
        ("---Select---","Prescription", "OTC", "Supplement")
    )

    
    
    if st.button("Add Medication"):

        if not med_name:
            st.warning('Please enter a medication name')

        elif not active_ingr:
            st.warning('Please enter active ingredients')

        elif dosage == "---Select---":
            st.warning('Please select a dosage frequency')
        
        elif instructions == "---Select---":
            st.warning('Please select medication instructions')
        
        elif not instructions:
            st.warning('Please specify your instructions')
        
        elif urge_lvl == "---Select---":
            st.warning('Please select an urgency level')
        
        elif med_category == "---Select---":
            st.warning('Please select a medication category')

        else:
            medication = {
                    
                    'Medication Name': med_name,
                    'Active Ingredients': active_ingr,
                    'Dosage Frequency': dosage,
                    'Instructions': instructions,
                    'Urgency Level': urge_lvl,
                    'Medication Category': med_category
                     
                     }
            new_df = pd.DataFrame([medication])

            old_df = st.session_state['medications']
            
            updated_df = pd.concat([old_df, new_df], ignore_index=True)

            st.session_state['medications'] = updated_df

            updated_df.to_csv("medications.csv", index=False)

            st.dataframe(updated_df)
        
            st.success('Medication Added!')

        

            

elif page == 'Interaction Check':
    st.header('Interaction Check')

    ingredient = st.text_input('Please Enter an Active Ingredient')

    if st.button('Check Ingredient'):

        if ingredient:
            
            
            
            df = st.session_state['medications']
            
            if df.empty:
                
                st.warning('No medications found. Please add a medication first.')
                
                st.stop()
                
            matches = []

            for i in range(len(df)):
                active_ingr = df['Active Ingredients'].iloc[i]
                med_name = df['Medication Name'].iloc[i]

                if ingredient.lower() in str(active_ingr).lower():
                    matches.append(med_name)

            st.write('Searching for:', ingredient)

            if len(matches) > 1:
                st.warning('Multiple medications contain this active ingredient!')
                st.write('Medications:', ', '.join(matches))

            elif len(matches) == 1:
                st.info('Matching medication: ' + str(matches[0]))

            else:
                st.info('No matching medications found.')


elif page == 'Daily Schedule':
    st.header('Daily Schedule')
    
    daily_schedule = st.session_state['medications']

    if daily_schedule.empty:
        
        st.warning('No medications found. Please add a medication first.')
        st.stop()
    
    
    schedule = daily_schedule[['Medication Name', 'Dosage Frequency', 'Instructions',
                               'Urgency Level']]

    st.dataframe(schedule)

    select_med = st.selectbox('Select a Medication', daily_schedule['Medication Name'])
    
    select_time = st.time_input('Select a Medication Time ')

    if st.button('Save Schedule'):

        med_schedule = {

            'Medication Name': select_med,
            'Medication Time': select_time,
            'Date': str(date.today())
            
        }

        time_df = pd.DataFrame([med_schedule])

        if os.path.exists('schedule.csv'):
            old_df = pd.read_csv('schedule.csv')
        else:
            old_df = pd.DataFrame()

        updated_df = pd.concat([old_df, time_df], ignore_index=True)

        updated_df.to_csv("schedule.csv", index=False)

        st.success('Schedule Saved!')


    if os.path.exists('schedule.csv'):
        saved_schedule = pd.read_csv('schedule.csv')

        today = str(date.today())

        if 'Date' in saved_schedule.columns:

            today_schedule = saved_schedule[saved_schedule['Date'] == today]

            st.subheader("Today's Medication Schedule")

            st.dataframe(today_schedule)

        else:
            st.warning('Please save a new schedule with a date.')
elif page == 'Inventory':
    st.header ('Inventory')

    updated_file = st.file_uploader('upload medication',type='csv')

    if st.button('Load Uploaded CSV'):

        if updated_file is not None:
            
            updated_df = pd.read_csv(updated_file)

            st.session_state['medications'] = updated_df

            updated_df.to_csv('medications.csv', index=False)

            st.success('CSV loaded successfully!')

        else:
            
            st.warning('Please upload a CSV file first.')

    df = st.session_state['medications']

    if df.empty:
        
        st.warning('No Medication!! Please add medication first ')
        st.stop()
        
    st.subheader('Edit Medications')

    edited_df = st.data_editor(df)

    if st.button('Save Changes'):

        st.session_state['medications'] = edited_df

        edited_df.to_csv('medications.csv', index=False)
        
        st.success('Changes saved successfully!')

        df = edited_df

    csv_data = st.session_state['medications'].to_csv(index=False)

    st.download_button(
        
        'Download Medications CSV',
        data=csv_data,
        file_name='medications.csv',
        mime='text/csv'
    )

    
    category = st.selectbox(

        'Select Medication Category',
        ('All Medications', 'Prescription', 'OTC', 'Supplement')
        
    )

    
    if category == 'All Medications':
        
        st.dataframe(df)
    else:
        
        filtered_df = df[df['Medication Category'] == category]
        st.dataframe(filtered_df)
        


    st.subheader('Manage Medication Stock')

    select_med = st.selectbox(
        'Select Medication',
        df['Medication Name']
    )


    quantity = st.number_input(
        
        'Quantity Remaining',
        min_value=0,
        value=0,
        step=1
    
    )


    pills_per_dose = st.number_input(
        
        'Pills per Dose',
        min_value=1,
        value=1,
        step=1
    
    )


    selected_row = df[df['Medication Name'] == select_med]

    freq = selected_row['Dosage Frequency'].iloc[0]


    dosage_int = {
    'Once a day': 1,
    'Twice a day': 2,
    '3 times a day': 3,
    'Every 8 hours': 3,
    'Once a week': 1/7
    
    }


    dosage_per_day = dosage_int[freq]



    
    if st.button('Check Stock'):

        stock_in_days = quantity / (dosage_per_day * pills_per_dose)

        st.write(f'Remaining Days: {stock_in_days:.1f} days')

        if stock_in_days <= 7:

            refill_status = 'Refill Needed'
            st.warning('Refill needed soon!')

        else:

            refill_status = 'Stock Sufficient'
            st.success('You have enough medication.')

        df.loc[df['Medication Name'] == select_med, 'Refill Status'] = refill_status

        st.session_state['medications'] = df

        df.to_csv('medications.csv', index=False)




else:

    st.header('Dashboard')

    df = st.session_state['medications']

    if df.empty:
        st.warning('No medications found. Please add a medication first.')
        st.stop()

    total_medications = len(df)
    total_categories = len(df['Medication Category'].dropna().unique())

    if 'Refill Status' in df.columns:
        refills_needed = len(df[df['Refill Status'] == 'Refill Needed'])
    else:
        refills_needed = 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric('Total Medications', total_medications)

    with col2:
        st.metric('Categories', total_categories)

    with col3:
        st.metric('Refills Needed', refills_needed)


    st.subheader('Medication Categories')

    category_counts = df['Medication Category'].value_counts()

    fig, ax = plt.subplots(figsize=(6, 4))

    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)


    ax.pie(
        category_counts.values,
        labels=category_counts.index,
        autopct='%1.0f%%',
        startangle=90,
        pctdistance=0.8,
        textprops={'color': 'white'},
        wedgeprops={'width': 0.4, 'edgecolor': 'black'}
    )

    ax.set_title('Medication Distribution', color='white')

    st.pyplot(fig)
    plt.close(fig)

    st.subheader('Dosage Frequency')

    fig, ax = plt.subplots(figsize=(7, 4))

    fig.patch.set_alpha(0)
    ax.patch.set_alpha(0)

    sns.countplot(
        data=df,
        x='Dosage Frequency',
        ax=ax
    )

    ax.set_title('Medications by Dosage Frequency', color='white')
    ax.set_xlabel('Dosage Frequency', color='white')
    ax.set_ylabel('Number of Medications', color='white')

    ax.tick_params(axis='both', colors='white') 

    plt.xticks(rotation=45)
    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)



