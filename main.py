import pandas as pd
import duckdb as db
import os
import sys
sys.path.insert(0, 'src')
from agents.sql_agent import SQLAgent

def main():
    print("Hello from sql-agent!")
    #sys.path.append("../")

    retail_sales = pd.read_csv("./data/data.csv")
    db.register("retail_sales", retail_sales)

    sqla = SQLAgent(tbl_name="retail_sales", max_token=5000)
    sqla.ask_question("What are the top 15 products by total sales, the total sales should have just 2 decimals and should be ordered by sales in descending order?", verbose=True)



if __name__ == "__main__":
    main()
