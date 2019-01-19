import matplotlib as mpl
mpl.use("PS") #handles X11 server detection (required to run on console)
import numpy as np

from cde.evaluation.GoodnessOfFitResults import GoodnessOfFitResults
from cde.evaluation_runs import base_experiment

from ml_logger import logger

EXP_PREFIX = 'question3_NNvsCKDE_Arma_Skew'
RESULTS_FILE = 'results.pkl'




def question3():
    #todo: add KMN & MDN

    estimator_params = {
    'ConditionalKernelDensityEstimation':
      {
          'bandwidth_selection': ['normal_reference', 'cv_ml', 'cv_ls'],
          'random_seed': [22]
      },
    }

    simulators_params = {
        'ArmaJump': {
            'c': [0.1],
            'arma_a1': [0.9],
            'std': [0.05],
            'jump_prob': [0.05],
        },

        'SkewNormal': {

        }
    }

    observations = 100 * np.logspace(0, 6, num=7, base=2.0, dtype=np.int32)

    return estimator_params, simulators_params, observations


if __name__ == '__main__':
    estimator_params, simulators_params, observations = question3()
    load = base_experiment.launch_experiment(estimator_params, simulators_params, observations, EXP_PREFIX)

    if load:
        results_from_pkl_file = dict(logger.load_pkl_log(RESULTS_FILE))
        gof_result = GoodnessOfFitResults(single_results_dict=results_from_pkl_file)
        results_df = gof_result.generate_results_dataframe(base_experiment.KEYS_OF_INTEREST)

        graph_dicts = [
            {"estimator": "ConditionalKernelDensityEstimation"},
            {"estimator": "ConditionalKernelDensityEstimation"}
            ]

        gof_result.plot_metric(graph_dicts, metric="js_divergence")
        print(results_df)

