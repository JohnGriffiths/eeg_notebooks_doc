.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_tutorials_plot_08-FurtherAnalysis.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_tutorials_plot_08-FurtherAnalysis.py:


08: Further Analysis
====================

Analyze results from fitting power spectrum models.

Exploring Power Spectrum Model Results
--------------------------------------

So far we have explored how to parameterize neural power spectra as a method to extract
parameters of interest from data - in particular measuring aperiodic and periodic activity.

These measured parameters can then be examined within or between groups of interest,
and/or fed into further analysis to examine if, for example, these parameters
predict other behavioural or physiological features of interest.
Largely, it is up to you what to do after fitting power spectrum models, as it depends
on your questions of interest.

Here, we briefly introduce some analysis utilities that are included in the module,
and explore some simple analyses that can be done with model parameters.

To start, we will load and fit some example data, as well as simulate a group of
power spectra to fit with power spectrum models.



.. code-block:: default


    # General imports
    import numpy as np

    # Import the FOOOF and FOOOFGroup objects
    from fooof import FOOOF, FOOOFGroup

    # Import the Bands object, which is used to define frequency bands
    from fooof.bands import Bands

    # Import simulation code and utilities
    from fooof.sim.params import param_sampler
    from fooof.sim.gen import gen_group_power_spectra
    from fooof.sim.utils import set_random_seed

    # Import some analysis functions
    from fooof.analysis import get_band_peak_fm, get_band_peak_fg

    # Import utility to download and load example data
    from fooof.utils.download import load_fooof_data








Load and Fit Example Data
~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: default


    # Load examples data files needed for this example
    freqs = load_fooof_data('freqs.npy', folder='data')
    spectrum = load_fooof_data('spectrum.npy', folder='data')









.. code-block:: default


    # Fit a power spectrum model
    fm = FOOOF(peak_width_limits=[2, 8])
    fm.fit(freqs, spectrum, [3, 30])








Simulate and Fit Group Data
~~~~~~~~~~~~~~~~~~~~~~~~~~~



.. code-block:: default


    # Set random seed, for consistency generating simulated data
    set_random_seed(21)

    # Generate some simulated power spectra
    freqs, spectra = gen_group_power_spectra(n_spectra=10,
                                             freq_range=[3, 40],
                                             aperiodic_params=param_sampler([[20, 2], [35, 1.5]]),
                                             periodic_params=param_sampler([[], [10, 0.5, 2]]))









.. code-block:: default


    # Initialize a FOOOFGroup object with desired settings
    fg = FOOOFGroup(peak_width_limits=[1, 8], min_peak_height=0.05,
                    max_n_peaks=6, verbose=False)

    # Fit power spectrum models across the group of simulated power spectra
    fg.fit(freqs, spectra)








Analysis Utilities
------------------

The FOOOF module includes some analysis functions. Note that these utilities are
generally relatively simple utilities that assist in accessing and investigating
the model parameters.

In depth analysis of power spectrum model results is typically idiosyncratic to the goals of
the project, and so we consider that this will typically require custom code, and seek
here to offer the most general utilities, and not support all possible applications.
Here we demonstrate some of these utility functions covering very general use cases.


Analyzing Periodic Components
-----------------------------

We will start by analyzing the periodic components.
In particular, these utilities mostly serve to help organize and extract periodic
components, for example extracting peaks that fall within defined frequency bands.

This also includes using the :class:`~.Bands` object, that is provided
to store band definitions.



.. code-block:: default


    # Define frequency bands of interest
    bands = Bands({'theta' : [4, 8],
                   'alpha' : [8, 12],
                   'beta' : [15, 30]})








Extracting peaks from FOOOF Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :func:`~.get_band_peak_fm` function takes in a
:class:`~.FOOOF` object and extracts peak(s) from a requested frequency range.

You can optionally specify:

- whether to return one peak from the specified band, in which case the highest peak is
  returned, or whether to return all peaks from within the band
- whether to apply a minimum threshold to extract peaks, for example, to extract
  peaks only above some minimum power threshold



.. code-block:: default


    # Extract any alpha band peaks from the power spectrum model
    alpha = get_band_peak_fm(fm, bands.alpha)
    print(alpha)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [9.48375519 0.91782334 2.        ]




Extracting peaks from FOOOFGroup Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Similarly, the :func:`~.get_band_peak_fg` function can be used
to select peaks within specific frequency ranges, from :class:`~fooof.FOOOFGroup` objects.

Note that you can also apply a threshold to extract group peaks but, as discussed below,
this approach will only extract one peak per individual model in the FOOOFGroup object.



.. code-block:: default


    # Get all alpha peaks from a group of power spectrum models
    alphas = get_band_peak_fg(fg, bands.alpha)

    # Check out some of the alpha data
    print(alphas[0:5, :])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [[10.03969821  0.48627642  3.78825898]
     [10.03394582  0.4880723   3.82623256]
     [        nan         nan         nan]
     [10.04095459  0.49087164  3.81810626]
     [        nan         nan         nan]]




When selecting peaks from a group of model fits, we want to retain information about
which model each peak comes from.

To do so, the output of :func:`~.get_band_peak_fg` is organized
such that each row corresponds to a specific model fit. This means that returned array
has the shape [n_models, 3], and so the index of each row corresponds to the index of the
model from the FOOOFGroup object.

For this to work, at most 1 peak is extracted for each model fit within the specified band.
If more than 1 peak are found within the band, the peak with the highest power is extracted.
If no peaks are found, that row is filled with 'nan'.



.. code-block:: default


    # Check descriptive statistics of extracted peak data
    print('Alpha CF : {:1.2f}'.format(np.nanmean(alphas[:, 0])))
    print('Alpha PW : {:1.2f}'.format(np.nanmean(alphas[:, 1])))
    print('Alpha BW : {:1.2f}'.format(np.nanmean(alphas[:, 2])))





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Alpha CF : 10.03
    Alpha PW : 0.49
    Alpha BW : 3.81




Customizing Peak Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to do more customized extraction of peaks, for example, extracting all peaks
in a frequency band from each model in a FOOOFGroup object, you may need to use the
underlying functions that operate on arrays of peak parameters. To explore these functions,
check the listing in the API page.


A Note on Frequency Ranges
--------------------------

A benefit of fitting power spectrum models is that you do not have to define
a priori frequency ranges from which to extract peaks.

Nevertheless, it may still be useful to group extracted peaks into 'bands' of interest,
which is why the aforementioned functions are offered.

Since this frequency-range selection can be done after model fitting, we do recommend
checking the model results, for example by checking a histogram of the center frequencies
extracted across a group, in order to ensure the frequency ranges you choose reflect
the characteristics of the data under study.


Analyzing the Aperiodic Component
---------------------------------

Typically, for analyzing the aperiodic component of the data, aperiodic parameters
just need to be extracted from FOOOF objects and fit into analyses of interest.



.. code-block:: default


    # Plot from the FOOOFGroup, to visualize the parameters
    fg.plot()




.. image:: /auto_tutorials/images/sphx_glr_plot_08-FurtherAnalysis_001.png
    :class: sphx-glr-single-img






.. code-block:: default


    # Extract aperiodic exponent data from group results
    exps = fg.get_params('aperiodic_params', 'exponent')

    # Check out the aperiodic exponent results
    print(exps)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [1.5174819  1.5180664  1.99827884 1.51563434 2.00559925 2.01700177
     2.00089211 2.02010911 1.51575116 1.99955831]




Example Analyses
----------------

Once you have extracted the parameters you can analyze them by, for example:

- Characterizing periodic & aperiodic properties,
  and analyzing spatial topographies, across demographics, modalities, and tasks
- Comparing peaks within and between subjects across different tasks of interest
- Predicting disease state based on power spectrum model parameters
- Fitting power spectrum models in a trial-by-trial approach to try and decode task
  properties, and behavioral states

So far we have only introduced the basic utilities to help with selecting and
examining power spectrum model parameters.

To further explore some of these specific analyses, and explore other
utilities that may be useful, check out the
`examples <https://fooof-tools.github.io/fooof/auto_examples/index.html>`_
page.


Conclusion
----------

This is the end of the main tutorial materials!

If you are having any troubles, please submit an issue on Github
`here <https://github.com/fooof-tools/fooof>`_,
and/or get in contact with us at voytekresearch@gmail.com.



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  1.039 seconds)


.. _sphx_glr_download_auto_tutorials_plot_08-FurtherAnalysis.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_08-FurtherAnalysis.py <plot_08-FurtherAnalysis.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_08-FurtherAnalysis.ipynb <plot_08-FurtherAnalysis.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
