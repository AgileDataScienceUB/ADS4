import plotsA as plA


### Test A ###

train="./data_sets/MFG10YearTerminationData-S.csv"
pathsA=plA.generate_plotsA_files(train)

#### Test B####
import plotsB as plB
import pandas as pd
import numpy as np
import pickle as pk
test_data_path="./data_sets/MFG10YearTerminationData_test-S.csv"
predictions_path="./data_sets/fake_predictions.p"

df=pd.read_csv(test_data_path)
n=df.shape[0]

pred=np.random.uniform(size=n) ##generating a pickle of fake predictions
pk.dump( pred, open( predictions_path, "wb" ) )

pathsB=plB.generate_plotsB_files(test_data_path,predictions_path)

