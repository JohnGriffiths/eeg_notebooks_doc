.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_tutorials_plot_06-FOOOFGroup.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_tutorials_plot_06-FOOOFGroup.py:


06: FOOOFGroup
==============

Using FOOOFGroup to run fit models across multiple power spectra.


.. code-block:: default


    # Import the FOOOFGroup object
    from fooof import FOOOFGroup

    # Import utility to download and load example data
    from fooof.utils.download import load_fooof_data








Fitting Multiple Spectra
------------------------

So far, we have explored using the :class:`~fooof.FOOOF` object to fit individual power spectra.

However, many potential use cases will have many power spectra to fit.

To support this, here we will introduce the :class:`~fooof.FOOOFGroup` object, which
applies the model fitting procedure across multiple power spectra.



.. code-block:: default


    # Load examples data files needed for this example
    freqs = load_fooof_data('group_freqs.npy', folder='data')
    spectra = load_fooof_data('group_powers.npy', folder='data')








For parameterizing a group of spectra, we can use a 1d array of frequency values
corresponding to a 2d array for power spectra, as is the organization of the data we loaded.



.. code-block:: default


    # Check the shape of the loaded data
    print(freqs.shape)
    print(spectra.shape)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    (100,)
    (25, 100)




FOOOFGroup
----------

The :class:`~fooof.FOOOFGroup` object is very similar to the FOOOF object (programmatically,
it inherits from the FOOOF object), and can be used in the same way.

The main difference is that instead of running across a single power spectrum, it
operates across 2D matrices containing multiple power spectra.

Note that by 'group' we mean merely to refer to a group of power-spectra. We
are not using the term 'group' in terms of necessarily referring to multiple subjects
or any particular idea of what a 'group' may be. A group of power spectra could
be spectra from across channels, or across trials, or across subjects, or
whatever organization makes sense for the analysis at hand.

The main differences with the :class:`~fooof.FOOOFGroup` object, are that it uses a
`power_spectra` attribute, which stores the matrix of power-spectra to be fit,
and collects fit results into a `group_results` attribute.

Otherwise, FOOOFGroup supports all the same functionality,
accessed in the same way as the FOOOF object.

Internally, it runs the exact same fitting procedure, per spectrum, as the FOOOF object.



.. code-block:: default


    # Initialize a FOOOFGroup object, which accepts all the same settings as FOOOF
    fg = FOOOFGroup(peak_width_limits=[1, 8], min_peak_height=0.05, max_n_peaks=6)









.. code-block:: default


    # Fit a group of power spectra with the .fit() method
    #  The key difference (compared to FOOOF) is that it takes a 2D array of spectra
    #     This matrix should have the shape of [n_spectra, n_freqs]
    fg.fit(freqs, spectra, [3, 30])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Running FOOOFGroup across 25 power spectra.





.. code-block:: default


    # Print out results
    fg.print_results()





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ==================================================================================================
                                                                                                  
                                           FOOOF - GROUP RESULTS                                      
                                                                                                  
                                 Number of power spectra in the Group: 25                             
                                                                                                  
                            The model was run on the frequency range 3 - 30 Hz                        
                                     Frequency Resolution is 0.49 Hz                                  
                                                                                                  
                                  Power spectra were fit without a knee.                              
                                                                                                  
                                          Aperiodic Fit Values:                                       
                            Exponents - Min:  0.353, Max:  0.982, Mean: 0.664                         
                                                                                                  
                             In total 85 peaks were extracted from the group                          
                                                                                                  
                                         Goodness of fit metrics:                                     
                                R2s -  Min:  0.902, Max:  0.990, Mean: 0.970                          
                             Errors -  Min:  0.025, Max:  0.121, Mean: 0.042                          
                                                                                                  
    ==================================================================================================





.. code-block:: default


    # Plot a summary of the results across the group
    fg.plot()




.. image:: /auto_tutorials/images/sphx_glr_plot_06-FOOOFGroup_001.png
    :class: sphx-glr-single-img





Just as with the FOOOF object, you can call the convenience method
:meth:`fooof.FOOOFGroup.report` to run the fitting, and print results & plots,
printing out the same as above.



.. code-block:: default


    # You can also save out PDFs reports for FOOOFGroup fits, same as with FOOOF
    fg.save_report('FOOOFGroup_report')








FOOOFGroup Results
------------------

FOOOFGroup collects fits across power spectra, and stores them in an attribute
called ``group_results``, which is a list of FOOOFResults objects.



.. code-block:: default


    # Check out some of the results stored in 'group_results'
    print(fg.group_results[0:2])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [FOOOFResults(aperiodic_params=array([-21.5931594 ,   0.66654701]), peak_params=array([[ 9.4088037 ,  1.44223656,  2.1352059 ],
           [18.44689676,  0.62328342,  2.36122321]]), r_squared=0.9729477049342996, error=0.05410881194674272, gaussian_params=array([[ 9.4088037 ,  1.45321198,  1.06760295],
           [18.44689676,  0.62588664,  1.18061161]])), FOOOFResults(aperiodic_params=array([-21.64485744,   0.78116378]), peak_params=array([[ 9.34931443,  1.59788754,  2.05215068],
           [11.57383428,  0.44989783,  1.24937295],
           [18.5393173 ,  0.73999236,  2.37682557]]), r_squared=0.9795689271205626, error=0.05326551715353906, gaussian_params=array([[ 9.34931443,  1.6014178 ,  1.02607534],
           [11.57383428,  0.34781375,  0.62468648],
           [18.5393173 ,  0.74005425,  1.18841278]]))]




get_params
~~~~~~~~~~

To collect data across all model fits, and to select specific data results from this data
you can should the :func:`~fooof.FOOOFGroup.get_params` method.

This method works the same as in the :class:`~fooof.FOOOF` object, and lets you extract
specific results by specifying a field, as a string, and (optionally) a specific column
of that data.

Since the :class:`~fooof.FOOOFGroup` object collects results from across multiple model fits,
you should always use :func:`~fooof.FOOOFGroup.get_params` to access parameter fits.
The result attributes introduced with the FOOOF object do not store results across the group,
as they are defined for individual model fits (and used internally as such by the
FOOOFGroup object).



.. code-block:: default


    # Extract aperiodic data
    aps = fg.get_params('aperiodic_params')
    exps = fg.get_params('aperiodic_params', 'exponent')

    # Extract peak data
    peaks = fg.get_params('peak_params')
    cfs = fg.get_params('peak_params', 'CF')

    # Extract metadata about the model fit
    errors = fg.get_params('error')
    r2s = fg.get_params('r_squared')









.. code-block:: default


    # The full list of data you can specify is available in the documentation of `get_params`
    print(fg.get_params.__doc__)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Return model fit parameters for specified feature(s).

            Parameters
            ----------
            name : {'aperiodic_params', 'peak_params', 'gaussian_params', 'error', 'r_squared'}
                Name of the data field to extract across the group.
            col : {'CF', 'PW', 'BW', 'offset', 'knee', 'exponent'} or int, optional
                Column name / index to extract from selected data, if requested.
                Only used for name of {'aperiodic_params', 'peak_params', 'gaussian_params'}.

            Returns
            -------
            out : ndarray
                Requested data.

            Raises
            ------
            NoModelError
                If there are no model fit results available.
            ValueError
                If the input for the `col` input is not understood.

            Notes
            -----
            For further description of the data you can extract, check the FOOOFResults documentation.
        




More information about the data you can extract is also documented in the FOOOFResults object.



.. code-block:: default


    # Grab a particular FOOOFResults item
    #  Note that as a shortcut, you can index the FOOOFGroup object directly to access 'group_results'
    f_res = fg[0]

    # Check the documentation for the FOOOFResults - with full descriptions of the resulting data
    print(f_res.__doc__)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Model results from parameterizing a power spectrum.

        Parameters
        ----------
        aperiodic_params : 1d array
            Parameters that define the aperiodic fit. As [Offset, (Knee), Exponent].
            The knee parameter is only included if aperiodic is fit with knee.
        peak_params : 2d array
            Fitted parameter values for the peaks. Each row is a peak, as [CF, PW, BW].
        r_squared : float
            R-squared of the fit between the full model fit and the input data.
        error : float
            Error of the full model fit.
        gaussian_params : 2d array
            Parameters that define the gaussian fit(s).
            Each row is a gaussian, as [mean, height, standard deviation].

        Notes
        -----
        This object is a data object, based on a NamedTuple, with immutable data attributes.
    





.. code-block:: default


    # Check out the extracted exponent values
    #  Note that this extraction will return an array of length equal to the number of model fits
    #    The model fit from which each data element originated is the index of this array
    print(exps)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [0.66654701 0.78116378 0.97596317 0.35626808 0.6622201  0.58348649
     0.76028334 0.46594578 0.70975764 0.60541613 0.73824337 0.39581645
     0.70797691 0.63143897 0.78995518 0.5037686  0.83825231 0.62707641
     0.72882427 0.71863453 0.74302615 0.8814779  0.35305536 0.39947468
     0.98214345]





.. code-block:: default


    # Check out some of the fit center-frequencies
    #  Note when you extract peak data, an extra column is returned,
    #  specifying which model fit it came from
    print(cfs[0:10, :])





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    [[ 9.4088037   0.        ]
     [18.44689676  0.        ]
     [ 9.34931443  1.        ]
     [11.57383428  1.        ]
     [18.5393173   1.        ]
     [ 9.48181066  2.        ]
     [11.25615368  2.        ]
     [12.57271821  2.        ]
     [18.67595773  2.        ]
     [10.61406527  3.        ]]




Saving & Loading with FOOOFGroup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

FOOOFGroup also support saving and loading, with same options as saving from the FOOOF object.

The only difference in saving FOOOFGroup, is that it saves out a 'jsonlines' file,
in which each line is a JSON object, saving the specified data and results for
a single power spectrum.



.. code-block:: default


    # Save out FOOOFGroup settings & results
    fg.save('FG_results', save_settings=True, save_results=True)









.. code-block:: default


    # You can then reload this group data
    nfg = FOOOFGroup()
    nfg.load('FG_results')









.. code-block:: default


    # Print results to check that the loaded group
    nfg.print_results()





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ==================================================================================================
                                                                                                  
                                           FOOOF - GROUP RESULTS                                      
                                                                                                  
                                 Number of power spectra in the Group: 25                             
                                                                                                  
                            The model was run on the frequency range 3 - 30 Hz                        
                                     Frequency Resolution is 0.49 Hz                                  
                                                                                                  
                                  Power spectra were fit without a knee.                              
                                                                                                  
                                          Aperiodic Fit Values:                                       
                            Exponents - Min:  0.353, Max:  0.982, Mean: 0.664                         
                                                                                                  
                             In total 85 peaks were extracted from the group                          
                                                                                                  
                                         Goodness of fit metrics:                                     
                                R2s -  Min:  0.902, Max:  0.990, Mean: 0.970                          
                             Errors -  Min:  0.025, Max:  0.121, Mean: 0.042                          
                                                                                                  
    ==================================================================================================




Parallel Support
~~~~~~~~~~~~~~~~

FOOOFGroup also has support for running in parallel, which can speed things up as
each power spectrum is fit independently.

The fit method includes an optional parameter ``n_jobs``, which if set at 1 (as default),
will fit models linearly (one at a time, in order). If you set this parameter to some other
integer, fitting will launch 'n_jobs' number of jobs, in parallel. Setting n_jobs to -1 will
launch model fitting in parallel across all available cores.

Note, however, that fitting power spectrum models in parallel does not guarantee a quicker
runtime overall. The computation time per model fit scales with the frequency range fit over,
and the 'complexity' of the power spectra, in terms of number of peaks. For relatively small
numbers of power spectra (less than ~100), across relatively small frequency ranges
(say ~3-40Hz), running in parallel may offer no appreciable speed up.



.. code-block:: default


    # Fit power spectrum models across a group of power spectra in parallel, using all cores
    fg.fit(freqs, spectra, n_jobs=-1)





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Running FOOOFGroup across 25 power spectra.




Progress Bar
~~~~~~~~~~~~

If you have a large number of spectra to fit with a :class:`~fooof.FOOOFGroup`, and you
want to monitor it's progress, you can also use a progress bar to print out fitting progress.

Progress bar options are:

- ``tqdm`` : a progress bar for running in terminals
- ``tqdm.notebook`` : a progress bar for running in Jupyter notebooks



.. code-block:: default


    # Fit power spectrum models across a group of power spectra, printing a progress bar
    fg.fit(freqs, spectra, progress='tqdm')





.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    Running FOOOFGroup:   0%|          | 0/25 [00:00<?, ?it/s]    Running FOOOFGroup:  12%|#2        | 3/25 [00:00<00:01, 13.71it/s]    Running FOOOFGroup:  16%|#6        | 4/25 [00:00<00:01, 10.84it/s]    Running FOOOFGroup:  20%|##        | 5/25 [00:00<00:04,  4.79it/s]    Running FOOOFGroup:  24%|##4       | 6/25 [00:00<00:03,  5.61it/s]    Running FOOOFGroup:  32%|###2      | 8/25 [00:01<00:02,  6.85it/s]    Running FOOOFGroup:  36%|###6      | 9/25 [00:01<00:02,  5.92it/s]    Running FOOOFGroup:  44%|####4     | 11/25 [00:01<00:01,  7.05it/s]    Running FOOOFGroup:  52%|#####2    | 13/25 [00:01<00:01,  7.81it/s]    Running FOOOFGroup:  60%|######    | 15/25 [00:01<00:01,  8.92it/s]    Running FOOOFGroup:  68%|######8   | 17/25 [00:02<00:01,  4.47it/s]    Running FOOOFGroup:  72%|#######2  | 18/25 [00:03<00:01,  4.43it/s]    Running FOOOFGroup:  80%|########  | 20/25 [00:03<00:00,  5.20it/s]    Running FOOOFGroup:  88%|########8 | 22/25 [00:03<00:00,  5.77it/s]    Running FOOOFGroup:  92%|#########2| 23/25 [00:03<00:00,  6.04it/s]    Running FOOOFGroup:  96%|#########6| 24/25 [00:03<00:00,  6.75it/s]    Running FOOOFGroup: 100%|##########| 25/25 [00:03<00:00,  6.57it/s]




Extracting Individual Fits
~~~~~~~~~~~~~~~~~~~~~~~~~~

When fitting power spectrum models for a group of power spectra, results are stored
in FOOOFResults objects, which store (only) the results of the model fit,
not the full model fits themselves.

To examine individual model fits, :class:`~fooof.FOOOFGroup` can regenerate
:class:`~fooof.FOOOF` objects for individual power spectra, with the full model available
for visualization. To do so, you can use the :meth:`~fooof.FOOOFGroup.get_fooof` method.



.. code-block:: default


    # Extract a particular spectrum, specified by index
    #  Here we also specify to regenerate the the full model fit, from the results
    fm = fg.get_fooof(ind=2, regenerate=True)









.. code-block:: default


    # Print results and plot extracted model fit
    fm.print_results()
    fm.plot()




.. image:: /auto_tutorials/images/sphx_glr_plot_06-FOOOFGroup_002.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ==================================================================================================
                                                                                                  
                                       FOOOF - POWER SPECTRUM MODEL                                   
                                                                                                  
                            The model was run on the frequency range 1 - 50 Hz                        
                                     Frequency Resolution is 0.49 Hz                                  
                                                                                                  
                                Aperiodic Parameters (offset, exponent):                              
                                             -21.1789, 1.0581                                         
                                                                                                  
                                           6 peaks were found:                                        
                                    CF:   7.18, PW:  0.292, BW:  1.00                                 
                                    CF:   9.38, PW:  1.347, BW:  1.74                                 
                                    CF:  11.07, PW:  0.722, BW:  1.17                                 
                                    CF:  12.17, PW:  0.340, BW:  3.82                                 
                                    CF:  18.50, PW:  0.708, BW:  1.90                                 
                                    CF:  19.97, PW:  0.376, BW:  5.52                                 
                                                                                                  
                                         Goodness of fit metrics:                                     
                                        R^2 of model fit is 0.9940                                    
                                        Error of the fit is 0.0304                                    
                                                                                                  
    ==================================================================================================




Conclusion
----------

Now we have explored fitting power spectrum models and running these fits across multiple
power spectra. Next we dig deeper into how to choose and tune the algorithm settings,
and how to troubleshoot if any of the fitting goes wrong.



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  9.638 seconds)


.. _sphx_glr_download_auto_tutorials_plot_06-FOOOFGroup.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_06-FOOOFGroup.py <plot_06-FOOOFGroup.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_06-FOOOFGroup.ipynb <plot_06-FOOOFGroup.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
