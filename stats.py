import sys
import csv
import time 
import argparse 

import pandas as pd
import matplotlib.pyplot as plt 

def joshPerMonth(joshlog): 
    timestamps = []
    with open(joshlog, 'r') as f: 
        reader = csv.reader(f)
        for line in reader:
            cast = int(line[0]) 
            spam_timestamp_start = 1713630509
            spam_timestamp_end = 1715226689
            if cast >= spam_timestamp_start and cast <= spam_timestamp_end: 
                if line[1] == '392796102132367364': 
                    continue 


            if line[2] == "1":
                timestamps.append(int(line[0]))
    
    plt.style.use("Solarize_Light2")
    df = pd.DataFrame({'Timestamp': pd.to_datetime(timestamps, unit='s')})
    # Extract year and month for grouping
    df['Year'] = df['Timestamp'].dt.year
    df['Month'] = df['Timestamp'].dt.month

    # Group by Year and Month
    grouped = df.groupby(['Year', 'Month']).count()

    # Rename the column for clarity
    grouped.rename(columns={'Timestamp': 'Count'}, inplace=True)

    # Reset index to use for plotting
    grouped.reset_index(inplace=True)

    # Create a new column for the formatted date label
    grouped['Date Label'] = grouped['Month'].apply(lambda x: pd.to_datetime(x, format='%m').strftime('%b')) + ' ' + grouped['Year'].astype(str)

    # Set 'Date Label' as the new index
    grouped.set_index('Date Label', inplace=True)

    average_count = grouped['Count'].mean()

    # Plotting
    plt.figure(figsize=(16,6))
    grouped['Count'].plot(kind='bar')
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.title('Josh per month')
    plt.ylabel('Count')
    plt.xlabel('Month, Year')
    plt.axhline(y=average_count, color='r', linestyle='--', label=f'Average: {average_count:.2f}')
    plt.xticks(rotation=45)
    plt.legend()
    plt.savefig('joshpermonth.png', dpi=300)

def avgJoshPerMonthUser(joshlog, usertable):
    users = {}
    with open(usertable, 'r') as f: 
        reader = csv.reader(f)
        for line in reader:
            users[line[0]] = line[1]

    data = []
    with open(joshlog, 'r') as f: 
        reader = csv.reader(f)
        for line in reader: 
            if line[1] not in users: 
                continue 

            cast = int(line[0]) 
            spam_timestamp_start = 1713630509
            spam_timestamp_end = 1715226689
            if cast >= spam_timestamp_start and cast <= spam_timestamp_end: 
                if line[1] == '392796102132367364': 
                    continue 

            data.append([int(line[0]), users[line[1]]])

    # convert to dataframe 
    df = pd.DataFrame(data, columns=['Timestamp', 'Username'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

    # Count events per user
    grouped = df.groupby('Username').size().reset_index(name='Count')

    # Calculate the average events per user
    average_count = grouped['Count'].mean()

    # Plotting
    plt.style.use('Solarize_Light2')
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.bar(grouped['Username'], grouped['Count'], color='skyblue')
    plt.axhline(y=average_count, color='r', linestyle='--', label=f'Average: {average_count:.2f}')
    plt.title('Number of Josh Events per User')
    plt.ylabel('Count of Events')
    plt.xlabel('Username')
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig('joshtotal.png', dpi=300)

def joshPerDayLastThirtyDays(joshlog, usertable): 
    users = {}
    with open(usertable, 'r') as f: 
        reader = csv.reader(f)
        for line in reader:
            users[line[0]] = line[1]

    THIRTY_DAYS_IN_SECONDS = 30 * 24 * 3600 
    now = int(time.time()) - THIRTY_DAYS_IN_SECONDS
    data = [] 
    with open(joshlog, 'r') as f: 
        reader = csv.reader(f)
        for line in reader:
            if int(line[0]) < now: 
                continue 
            if line[1] not in users: 
                continue 
            data.append([int(line[0]), users[line[1]]]) 

    df = pd.DataFrame(data, columns=['Timestamp', 'Username'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

    grouped = df.groupby('Username').size().reset_index(name='Count')

    # Calculate the average events per user
    average_count = grouped['Count'].mean()

    # Plotting
    plt.style.use('Solarize_Light2')
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.bar(grouped['Username'], grouped['Count'], color='skyblue')
    plt.axhline(y=average_count, color='r', linestyle='--', label=f'Average: {average_count:.2f}')
    plt.title("Number of Josh's: Last 30 Days")
    plt.ylabel('Josh Count')
    plt.xlabel('Username')
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig('last_thirty_days.png', dpi=300)

def lastNDays(joshlog, usertable, days): 
    users = {}
    with open(usertable, 'r') as f: 
        reader = csv.reader(f)
        for line in reader:
            users[line[0]] = line[1]

    DAYS_IN_SECONDS = days * 24 * 3600 
    timeframe = int(time.time()) - DAYS_IN_SECONDS
    data = [] 
    with open(joshlog, 'r') as f: 
        reader = csv.reader(f)
        for line in reader:
            if int(line[0]) < timeframe: 
                continue 
            if line[1] not in users: 
                continue 
            data.append([int(line[0]), users[line[1]]]) 

    df = pd.DataFrame(data, columns=['Timestamp', 'Username'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')

    grouped = df.groupby('Username').size().reset_index(name='Count')

    # Calculate the average events per user
    average_count = grouped['Count'].mean()

    # Plotting
    plt.style.use('Solarize_Light2')
    plt.gcf().subplots_adjust(bottom=0.2)
    plt.bar(grouped['Username'], grouped['Count'], color='skyblue')
    plt.axhline(y=average_count, color='r', linestyle='--', label=f'Average: {average_count:.2f}')
    plt.title("Number of Josh's: Last " + str(days) + " Days")
    plt.ylabel('Josh Count')
    plt.xlabel('Username')
    plt.legend()
    plt.xticks(rotation=45)
    plt.savefig('last_'+str(days)+'_days.png', dpi=300)


def main(): 
    parser = argparse.ArgumentParser(
                    prog='joshtats',
                    description='Generates graphs from input josh tables',
                    epilog='josh')
    
    parser.add_argument('joshlog', help='the joshlog csv table')           # positional argument
    parser.add_argument('--usertable', help='the user csv table')
    parser.add_argument('--num_days', help='The number of days used for the `lastn` option.')
    parser.add_argument('option', help='the graph type wanted. Options are: totaljoshpermonth, totaljosh, joshlastthirty, lastn')

    args = parser.parse_args()
    option = args.option 
    joshlog = args.joshlog 
    usertable = args.usertable
    num_days = args.num_days 

    if option == 'totaljoshpermonth':
        joshPerMonth(joshlog)
    elif option == 'totaljosh':
        if usertable == None: 
            print('Usertable must be specified')
            exit(1) 
        avgJoshPerMonthUser(joshlog, usertable)
    elif option == 'joshlastthirty':
        if usertable == None: 
            print('Usertable must be specified')
            exit(1) 
        joshPerDayLastThirtyDays(joshlog, usertable)
    elif option == 'lastn':
        if usertable == None: 
            print('Usertable must be specified')
            exit(1)
        elif num_days == None or int(num_days) <= 0: 
            print('Number of days must be specified and a strictly positive integer')
            exit(1)
        lastNDays(joshlog, usertable, int(num_days))

    else: 
        print('invalid option. Use help flag to see valid options')
        exit(1)

        

        
        

            
        
    


if __name__ == "__main__":
    main()