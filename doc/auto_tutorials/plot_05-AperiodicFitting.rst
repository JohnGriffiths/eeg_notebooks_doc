.. only:: html

    .. note::
        :class: sphx-glr-download-link-note

        Click :ref:`here <sphx_glr_download_auto_tutorials_plot_05-AperiodicFitting.py>`     to download the full example code
    .. rst-class:: sphx-glr-example-title

    .. _sphx_glr_auto_tutorials_plot_05-AperiodicFitting.py:


05: Aperiodic Component Fitting
===============================

Choosing and using different approaches for fitting the aperiodic component.


.. code-block:: default


    # Import the FOOOF object
    from fooof import FOOOF

    # Import utility to download and load example data
    from fooof.utils.download import load_fooof_data








Aperiodic Fitting Approaches
----------------------------

There are currently two approaches for fitting the aperiodic component:

- Fitting with just an offset and a exponent, equivalent to a linear fit in log-log space

  - `aperiodic_mode` = 'fixed'
- Including a 'knee' parameter, reflecting a fit with a bend, in log-log space

  - `aperiodic_mode` = 'knee'

Fitting in the 'fixed' mode assumes a single 1/f like characteristic to the aperiodic
component, meaning it looks linear across all frequencies in log-log space.

Though this assumption is true across *some* frequency ranges in neural data, it does
does not hold up across broad frequency ranges. If fitting is done in the 'fixed' mode,
but the assumption of a single 1/f is violated, then fitting will go wrong.

Broad frequency ranges (typically ranges greater than ~40 Hz range) don't meet this
criterion, as they typically exhibit a 'bend' in the aperiodic component, whereby there is
not a single 1/f property across all frequencies, but rather a 'bend' in the aperiodic
component. For these cases, fitting should be done using an extra parameter to capture
this, in 'knee' mode.


Fitting with an Aperiodic 'Knee'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's explore fitting power spectrum models across a broader frequency range,
using some local field potential data.



.. code-block:: default


    # Load example data files needed for this example
    freqs = load_fooof_data('freqs_lfp.npy', folder='data')
    spectrum = load_fooof_data('spectrum_lfp.npy', folder='data')









.. code-block:: default


    # Initialize a FOOOF object, setting the aperiodic mode to use a 'knee' fit
    fm = FOOOF(peak_width_limits=[2, 8], aperiodic_mode='knee')









.. code-block:: default


    # Fit a power spectrum model
    #  Note that this time we're specifying an optional parameter to plot in log-log
    fm.report(freqs, spectrum, [2, 70], plt_log=True)




.. image:: /auto_tutorials/images/sphx_glr_plot_05-AperiodicFitting_001.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ==================================================================================================
                                                                                                  
                                       FOOOF - POWER SPECTRUM MODEL                                   
                                                                                                  
                            The model was run on the frequency range 2 - 70 Hz                        
                                     Frequency Resolution is 1.00 Hz                                  
                                                                                                  
                             Aperiodic Parameters (offset, knee, exponent):                           
                                         6.5759, 87.2219, 2.0354                                      
                                                                                                  
                                           2 peaks were found:                                        
                                    CF:   7.98, PW:  0.806, BW:  2.03                                 
                                    CF:  16.32, PW:  0.233, BW:  2.29                                 
                                                                                                  
                                         Goodness of fit metrics:                                     
                                        R^2 of model fit is 0.9925                                    
                                        Error of the fit is 0.0405                                    
                                                                                                  
    ==================================================================================================




A note on interpreting the 'knee' parameter
-------------------------------------------

The aperiodic fit has the form:

.. math::
   AP = 10^b * \ \frac{1}{(k + F^\chi)}

The knee parameter reported above corresponds to `k` in the equation.

This parameter is dependent on the frequency at which the aperiodic fit
transitions from horizontal to negatively sloped.

To interpret this parameter as a frequency, take the :math:`\chi`-th root of `k`, i.e.:

.. math::
   knee \ frequency = k^{1/\ \chi}

Interpreting the fit results when using knee fits is more complex, as the exponent result is
no longer a simple measure of the aperiodic component as a whole, but instead reflects the
aperiodic component past the 'knee' inflecting point. Because of this, when doing knee fits,
knee & exponent values should be considered together.


Example: Aperiodic Fitting Gone Wrong
-------------------------------------

In the example above, we jumped directly to fitting with a knee.

Here we will explore what it looks like if we don't use the appropriate mode for fitting
the aperiodic component - fitting in 'fixed' mode when we should use 'knee'



.. code-block:: default


    # Create and fit a power spectrum model in fixed mode to the same data as above
    fm = FOOOF(peak_width_limits=[2, 8], aperiodic_mode='fixed')
    fm.report(freqs, spectrum, [2, 70], plt_log=True)




.. image:: /auto_tutorials/images/sphx_glr_plot_05-AperiodicFitting_002.png
    :class: sphx-glr-single-img


.. rst-class:: sphx-glr-script-out

 Out:

 .. code-block:: none

    ==================================================================================================
                                                                                                  
                                       FOOOF - POWER SPECTRUM MODEL                                   
                                                                                                  
                            The model was run on the frequency range 2 - 70 Hz                        
                                     Frequency Resolution is 1.00 Hz                                  
                                                                                                  
                                Aperiodic Parameters (offset, exponent):                              
                                              5.3476, 1.3360                                          
                                                                                                  
                                           3 peaks were found:                                        
                                    CF:   8.01, PW:  1.020, BW:  2.41                                 
                                    CF:  17.02, PW:  0.369, BW:  8.00                                 
                                    CF:  31.05, PW:  0.273, BW:  8.00                                 
                                                                                                  
                                         Goodness of fit metrics:                                     
                                        R^2 of model fit is 0.9847                                    
                                        Error of the fit is 0.0607                                    
                                                                                                  
    ==================================================================================================




In this case, we see that the 'fixed' aperiodic component (equivalent to a line
in log-log space) is not able to capture the data, which has a curve.

To compensate, the model adds extra peaks, but these are also not a good
characterization of the data.

In this example, the data, over this frequency range, needs to be fit in
'knee' mode to be able to appropriately characterize the data.


Choosing an Aperiodic Fitting Procedure
---------------------------------------

It is important to choose the appropriate aperiodic fitting approach for your data.

If there is a clear knee in the power spectrum, fitting in 'fixed' mode will not
work well. However fitting with a knee may perform sub-optimally in ambiguous cases
(where the data may or may not have a knee), or if no knee is present.

Given this, we recommend:

- Check your data, across the frequency range of interest,
  for what the aperiodic component looks like.

  - If it looks roughly linear (in log-log space), fit without a knee.

    - This is likely across smaller frequency ranges, such as 3-30.
    - Do not perform no-knee fits across a range in which this does not hold.
  - If there is a clear knee, then use knee fits.

    - This is likely across larger fitting ranges such as 1-150 Hz.
- Be wary of ambiguous ranges, where there may or may not be a knee.

  - Trying to fit without a knee, when there is not a single consistent aperiodic component,
    can lead to very bad fits. But it is also a known issue that trying to fit with a knee
    can lead to suboptimal fits when no knee is present.

    - We therefore currently recommend picking frequency ranges in which the expected
      aperiodic component process is relatively clear.


Conclusion
----------

We have now explored the :class:`~fooof.FOOOF` object, and different fitting
approaches for the aperiodic component. Next up, we will be introducing how
to scale the fitting to apply across multiple power spectra.



.. rst-class:: sphx-glr-timing

   **Total running time of the script:** ( 0 minutes  0.933 seconds)


.. _sphx_glr_download_auto_tutorials_plot_05-AperiodicFitting.py:


.. only :: html

 .. container:: sphx-glr-footer
    :class: sphx-glr-footer-example



  .. container:: sphx-glr-download sphx-glr-download-python

     :download:`Download Python source code: plot_05-AperiodicFitting.py <plot_05-AperiodicFitting.py>`



  .. container:: sphx-glr-download sphx-glr-download-jupyter

     :download:`Download Jupyter notebook: plot_05-AperiodicFitting.ipynb <plot_05-AperiodicFitting.ipynb>`


.. only:: html

 .. rst-class:: sphx-glr-signature

    `Gallery generated by Sphinx-Gallery <https://sphinx-gallery.github.io>`_
