import plotly.express as px
import pandas as pd
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("csv_path")
    parser.add_argument("-p", "--plot", action="store_true", help="")

    args = parser.parse_args()

    df: pd.DataFrame = pd.read_csv(args.csv_path, names=["date", "description", "expenses", "income"])
    df.drop(columns=["description"], inplace=True)

    df["date"] = pd.to_datetime(df["date"])
    df = df.set_index("date")
    
    df = df.resample("D").sum()

    df['net_change'] = df['income'] - df['expenses']
    df['balance'] = df['net_change'].cumsum()

    print(df)

    if args.plot:
        fig = px.area(df, x=df.index, y=["balance", "income", "expenses"])
        fig.update_layout(title={'text': '<b>Financials</b>'})
        fig.show()