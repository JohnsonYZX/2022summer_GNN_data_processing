# Multi-view Data Processing

- **Input:** put all input files ended with ".view" into folder **data**.

- **Output:** all the output csv will be stored in folder **output** and statistic data will be stored in text **output_statistics.txt**.

- **Requirement File:** write all requirement in the text **data_requirement.txt**

  - **format:**  **input_file_name** + **" "** + **output_file_name** + **" "** + **cameras** + **" "** + **time**
  - **example:** /home/data/wushu/1.flv wushu 26 20

- **Running Code:** 

  ```
  python data_collecter.py
  ```

- **Note:** The format of output is exactly the same as the figure below, which means the first line of each table is empty.

![figure](https://github.com/JohnsonYZX/2022summer_GNN_data_processing/blob/main/figure.png)

