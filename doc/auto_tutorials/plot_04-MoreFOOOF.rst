.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_tutorials_plot_04-MoreFOOOF.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_tutorials_plot_04-MoreFOOOF.py:


04: Exploring the FOOOF Object
==============================

Further exploring the FOOOF object, including algorithm settings and available methods.


.. code-block:: default


    # Import the FOOOF object
    from fooof import FOOOF

    # Import utility to download and load example data
    from fooof.utils.download import load_fooof_data









.. code-block:: default


    # Initialize a FOOOF object
    fm = FOOOF()








Description of methods and attributes
-------------------------------------

The :class:`~fooof.FOOOF` object contents consist of 4 main components (groups of data / code):

- 1) settings attributes, that control the algorithm fitting
- 2) data attributes, that contain and describe the data
- 3) result attributes, that contain the results of the model fit
- 4) methods (functions) that perform procedures for fitting models and associated utilities

Each these which are described in more detail below.

The FOOOF module follows the following Python conventions:

- all user exposed settings, data, and methods are directly accessible through the object
- 'hidden' (internal) settings and methods have a leading underscore

  - you *can* access these if you need to, but one should be cautious doing so


1) Settings (attributes)
^^^^^^^^^^^^^^^^^^^^^^^^

There are a number of settings that control the fitting algorithm, that
can be set by the user when initializing the :class:`~fooof.FOOOF` object.

There are some internal settings that are not exposed at initialization.
These settings are unlikely to need to be accessed by the user, but can be if desired -
they are all defined and documented in \__init\__ (there should be no other settings, or
'magic numbers' in any other parts of the code).


Controlling Peak Fits
~~~~~~~~~~~~~~~~~~~~~

**peak_width_limits (Hz)** default: [0.5, 12]

Enforced limits on the minimum and maximum widths of extracted peaks, given as a list of
[minimum bandwidth, maximum bandwidth]. We recommend bandwidths be set to be at last twice
the frequency resolution of the power spectrum.


Peak Search Stopping Criteria
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An iterative procedure searches for candidate peaks in the flattened spectrum. Candidate
peaks are extracted in order of decreasing height, until some stopping criterion is met,
which is controlled by the following settings:

**max_n_peaks (int)** default: infinite

The maximum number of peaks that can be extracted from a given power spectrum. The algorithm
will halt searching for new peaks when this number is reached. Note that peaks are extracted
iteratively by height (over and above the aperiodic component), and so this approach will
extract (up to) the *n* largest peaks.

**peak_threshold (in units of standard deviation)** default: 2.0

The threshold, in terms of standard deviation of the aperiodic-removed power
spectrum, above which a data point must pass to be considered a candidate peak.
Once a candidate peak drops below this threshold, the peak search is halted (without
including the most recent candidate).

**min_peak_height (units of power - same as the input spectrum)** default: 0

The minimum height, above the aperiodic fit, that a peak must have to be extracted
in the initial fit stage. Once a candidate peak drops below this threshold, the peak
search is halted (without including the most recent candidate). Note that because
this constraint is enforced during peak search, and prior to final peak fit, returned
peaks are not guaranteed to surpass this value in height.

Note: there are two different height-related halting conditions for the peak searching.
By default, the relative (standard-deviation based) threshold is defined, whereas the
absolute threshold is set to zero (this default is because there is no general way to
set this value without knowing the scale of the data). If both are defined, both are
used and the peak search will halt when a candidate peak fails to pass either the absolute,
or relative threshold.

Aperiodic Mode
~~~~~~~~~~~~~~

**aperiodic_mode (string)** default='fixed'

The fitting approach to use for the aperiodic component.

Options:
  - 'fixed' : fits without a knee parameter (with the knee parameter 'fixed' at 0)
  - 'knee' : fits the full exponential equation, including the 'knee' parameter

Verbosity
~~~~~~~~~

**verbose (boolean)** default='True'

Whether to print out status updates and warnings.



.. code-block:: default


    # You can check all the user defined settings with check_settings
    #  The description parameter here is set to print out quick descriptions of the settings
    fm.print_settings(description=True)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ==================================================================================================
                                                                                                  
                                             FOOOF - SETTINGS                                         
                                                                                                  
                                     Peak Width Limits : (0.5, 12.0)                                  
                            Limits for minimum and maximum peak widths, in Hz.                        
                                        Max Number of Peaks : inf                                     
                              Maximum number of peaks that can be extracted.                          
                                        Minimum Peak Height : 0.0                                     
                    Minimum absolute height of a peak, above the aperiodic component.                 
                                           Peak Threshold: 2.0                                        
                   Relative threshold for minimum height required for detecting peaks.                
                                          Aperiodic Mode : fixed                                      
                         The approach taken for fitting the aperiodic component.                      
                                                                                                  
    ==================================================================================================




Changing Settings
~~~~~~~~~~~~~~~~~

Note that if you wish to change settings, then you should re-initialize
a new :class:`~fooof.FOOOF` object with new settings.

Simply changing the value of the relevant attribute may not appropriately propagate
the value, and thus may lead to a failure, either creating an error, or not applying
the settings properly during fit and returning erroneous results.

Here we will re-initialize a new FOOOF object, with some new settings.



.. code-block:: default


    # Re-initialize a new FOOOF object, with some specified settings
    fm = FOOOF(peak_width_limits=[1, 8], max_n_peaks=6, min_peak_height=0.15)








2) Data (attributes)
^^^^^^^^^^^^^^^^^^^^

The :class:`~fooof.FOOOF` object stores the following data attributes:

- ``freqs``: the frequency values corresponding to the data
- ``power_spectrum``: the power spectrum
- ``freq_range``: the frequency range of the data
- ``freq_res``: the frequency resolution of the data

During the fit procedure, interim (hidden) data variables are also created and used.

There is also an indicator attribute, ``has_data`` which indicates
if the current object has data loaded.



.. code-block:: default


    # Load example data files needed for this example
    freqs = load_fooof_data('freqs_2.npy', folder='data')
    spectrum = load_fooof_data('spectrum_2.npy', folder='data')









.. code-block:: default


    # Set a frequency range and add the data to the object
    freq_range = [2, 40]
    fm.add_data(freqs, spectrum, freq_range)









.. code-block:: default


    # Check if the object has data loaded
    print('Has data loaded: ', fm.has_data)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Has data loaded:  True





.. code-block:: default


    # Check out the data attributes in the object
    print('Frequency Range: \t', fm.freq_range)
    print('Frequency Resolution: \t', fm.freq_res)
    print('Frequency Values: \t', fm.freqs[0:5])
    print('Power Values: \t\t', fm.power_spectrum[0:5])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Frequency Range:         [2.441406250001353, 39.55078125002192]
    Frequency Resolution:    0.48828125000027045
    Frequency Values:        [2.44140625 2.9296875  3.41796875 3.90625    4.39453125]
    Power Values:            [-21.99921865 -21.99669556 -22.02605736 -21.96875308 -22.15436702]




Now that we have picked our settings, and added the data, let's fit a power spectrum model.



.. code-block:: default


    # Fit a power spectrum model to the loaded data
    fm.fit()








3) Results (attributes)
^^^^^^^^^^^^^^^^^^^^^^^

With our model fit, the results attributes should now hold values.

Recall that here we follow the scipy convention in that any attributes that contain
model results are indicated by a trailing underscore.

The model results stored by the object are:

- ``aperiodic_params_``: a list of aperiodic parameters, stored as [Offset, (Knee), Exponent]
- ``peak_params_``: all periodic parameters, where each row is a peak, as [CF, PW, BW]
- ``r_squared_``: the r-squared of the model, as compared to the original data
- ``error_``: the error of the model, as compared to the original data

Other attributes which store outputs from the model are:

- ``fooofed_spectrum_``: the full model reconstruction
- ``n_peaks_``: a helper attribute which indicates how many peaks were fit in the model

The :class:`~fooof.FOOOF` object also has an indicator attribute, ``has_model``
which indicates if the current object has model results available.



.. code-block:: default


    # Check if the object has model results
    print('Has model results: ', fm.has_model)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Has model results:  True





.. code-block:: default


    # Print out model fit results
    print('aperiodic params: \t', fm.aperiodic_params_)
    print('peak params: \t', fm.peak_params_)
    print('r-squared: \t', fm.r_squared_)
    print('fit error: \t', fm.error_)
    print('fooofed spectrum: \t', fm.fooofed_spectrum_[0:5])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    aperiodic params:        [-21.44372547   1.07510691]
    peak params:     [[ 9.81511897  0.72768575  3.00442116]
     [13.04276146  0.25957048  2.5434593 ]
     [18.12826732  0.15093637  4.62563212]]
    r-squared:       0.992299177438436
    fit error:       0.02937242314395825
    fooofed spectrum:        [-21.86047574 -21.9455885  -22.01750003 -22.07961578 -22.13385218]




4) Methods
^^^^^^^^^^

The :class:`~fooof.FOOOF` object contains a number of methods that are either used
to fit models and access data, and/or offer extra functionality.

In addition to the exposed methods, there are some internal private methods,
with a leading underscore in their name, that are called in the
fitting procedure. These methods should not be called directly by the user
as they may depend on internal state of the object as defined from other methods,
and so may not do as expected in isolation.



.. code-block:: default


    # This piece of code is just a way to print out all the public methods with their description
    [print(it + '\n\t' + eval('fm.' + it + '.__doc__').split('\n')[0]) \
        for it in dir(fm) if it[0] != '_' and callable(eval('fm.' + it))];





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    add_data
            Add data (frequencies, and power spectrum values) to the current object.
    add_meta_data
            Add data information into object from a FOOOFMetaData object.
    add_results
            Add results data into object from a FOOOFResults object.
    add_settings
            Add settings into object from a FOOOFSettings object.
    copy
            Return a copy of the current object.
    fit
            Fit the full power spectrum as a combination of periodic and aperiodic components.
    get_meta_data
            Return data information from the current object.
    get_params
            Return model fit parameters for specified feature(s).
    get_results
            Return model fit parameters and goodness of fit metrics.
    get_settings
            Return user defined settings of the current object.
    load
            Load in a FOOOF formatted JSON file to the current object.
    plot
            Plot the power spectrum and model fit results from a FOOOF object.
    print_report_issue
            Prints instructions on how to report bugs and/or problematic fits.
    print_results
            Print out model fitting results.
    print_settings
            Print out the current settings.
    report
            Run model fit, and display a report, which includes a plot, and printed results.
    save
            Save out data, results and/or settings from a FOOOF object into a JSON file.
    save_report
            Generate and save out a PDF report for a power spectrum model fit.
    set_debug_mode
            Set whether debug mode, wherein an error is raised if fitting is unsuccessful.

    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]



Saving Data & Results
~~~~~~~~~~~~~~~~~~~~~

There is also functionality for saving out, and loading back in, data and results.

You have the option to specify which data to save.

- `results`: model fit results (same as is returned in FOOOFResult)
- `settings`: all public settings (everything available at initialization)
- `data`: freqs & power spectrum

Selected items are saved out to JSON files. You can specify a file name to save
or append to, or pass in a JSON file object.



.. code-block:: default


    # Save out results, settings, and data
    fm.save('FOOOF_results', save_results=True, save_settings=True, save_data=True)









.. code-block:: default


    # Load back in the saved out information
    nfm = FOOOF()
    nfm.load('FOOOF_results')









.. code-block:: default


    # Plot loaded results
    nfm.plot()




.. image:: /auto_tutorials/images/sphx_glr_plot_04-MoreFOOOF_001.png
    :class: sphx-glr-single-img





Creating Reports
~~~~~~~~~~~~~~~~

There is also functionality to save out a 'report' of a particular model fit.

This generates and saves a PDF which contains the same output as
:meth:`~fooof.FOOOF.print_results`,
:meth:`~fooof.FOOOF.plot`, and
:meth:`~fooof.FOOOF.print_settings`.



.. code-block:: default


    # Save out a report of the current model fit & results
    fm.save_report('FOOOF_report')








Conclusion
----------

We have now fully explored the :class:`~fooof.FOOOF` object, and all it contains.
Next, we will take a deeper dive into how to choose different modes for fitting
the aperiodic component of power spectra.



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  2.020 seconds)


.. _sphx_glr_download_auto_tutorials_plot_04-MoreFOOOF.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_04-MoreFOOOF.py <plot_04-MoreFOOOF.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_04-MoreFOOOF.ipynb <plot_04-MoreFOOOF.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
