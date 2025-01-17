# List of todo's

publish ready:
    [x] Add in ClimaX -- Linear better than https://arxiv.org/abs/2301.10343
     -> not for now i'll do that in a paper.
    [x] correct author list
    [x] Mention FairGP for doing physics-informed ML
    [x] go over list of take-aways and check each off to see if it's in text
     -> i dont want to 
    [] clean todo.md
    [x] clean requirements.txt , delete environment.yaml (making sure streamlit still works)
        -> yes, streamlit uses requirements.txt so we should be all good.
    [] ask Lea to review the tutorial
    [] move fcnn, unet, etc. to either not be in dev branch and not in main (using proper git workflow) or move into archive/ folder
    [] move explore_xxx notebooks into dev branch
    [] fork dev branch into new climate-emulator-tutorial-private repo and delete from public repo.

clarify take-aways:
    [] for Earth scientists:
        1) decide functional form in-the-loop with data
        2) implement linear baseline
        3) ML will overfit internal variability
            --> need to illustrate those in a poster && notebook.
    [] co2, ch4, bc, so2 are a lot of greenhouse gases ->> there's more than co2 that impacts temperature. need common unit
        [] ml requires to specify in/ and outputs. problem is very different depending on how you conceptioanlize the problem. Is it all gases together, each gas individually, or just the policy?
        [] BC and SO2 have little variation in cmip. need to have scenarios that capture that.
        [] which variations are captured in the data in which not. We just have 5 scenarios, so we need to set-up the problem in a way that we have more data points.
            -> need to decide purpose // in-/ output relation // which functional form to learn
                -> is there enough data for this functional form from the ML pov. 
                -> can we take assumptions in model
    [] pitfall: use ML for problem where simpler is just fine.
        [] global CO2 -> annual local tas is mostly linear ->> need more difficult variables
        [] what are the learnings for ML ??  -->> need linear baseline
        [] relationships are just local??
    [] internal variability needs to be actively addressed ->> need ensemble members or temporal average
        [] ML will be able to get perfect fit, but probably overfit on the val set to get internal variability right. need internal variability plot.
    [] global co2 -> local tas has errors in Arctic, Antarctica in linear model. ->> need nonlinear to get rid of warming whole and time-history to get Greenland Sea
    [] global CO2 -> precip?? also mostly linear?

Beyond tutorial:
Results:
    [] why is the cnn-lstm better in the arctic than linear model?
        - is this due to long- short term memory?
        - what are the inputs to the cnn again? 
            global cum. co2 emission (t-10:t)
            global      ch4 emission (t-10:t)
            local       bc  emission (t-10:t)
            local       so2 emission (t-10:t)
            + latent state?
        - what are the outputs?
            local       tas          (t)
        - the Arctic signal is Not in the bc, so2 data
        - is this a result of data leakage -> probably not bc all of ssp245 is held-out.
        - Is the Arctic warming different for ssp370 and ssp585 at 4500GtCO2? The ssp245 has 4500GtCO2 in 2100; so a linear model in the Arctic will predict the average between ssp370(t=2070, co2=4050)  and ssp585(t=2050, co2=4050)
            - If the arctic warming is different for ssp370 and ssp585 that could explain why the CO2 history helps the CNN to predict arctic warming better 
                - Maybe a co2 value + gradient would be sufficient for that though:)
                    ----->>>>>> TEST:::::: DOES LINEAR MODEL[T(t), T(t)-T(t-1)] get Arctic warming right?
            - 4500 GtCO2 = co2(ssp245, 2100) = co2(ssp370,2070) = co2(ssp585,2050)
    [] Deeper exploration on regions where linear pattern scaling breaks down
        [] Does the linear assumption break down during rare events?
        could plot accuracy (y-axis) over pixel-wise binned TAS prediction value, where TAS prediction values are ordered according to frequency (or TAS if TAS itself is Gaussian distributed)
    [] How to deal with internal variability?
        [x] could smoothen global T and then map co2 onto global T
            -> I did this for the linear time-difference model.
        [] plot internal variability map
demo development
    [] expand piecewise linear to map all_ghg -> T
    [] use co2 emission over time curve.
        [] create co2(t) = by piecewise linear interpolation of co2(ssp127,ssp585(t))
        [] plot co2 emission curve
    [] add ch4, etc. as optional arguments at the bottom

model development:
    [] write FCNN baseline
        [] write train.py s.t., i can plug in an fcnn, unet, etc. given a dataloader?
            [] rewrite dataloader, s.t., the explore_data scipt saves an ML-ready dataset in processed/. The train.py then takes in a path to that dataset and creates a dataloader.
            [] rewrite criterion s.t., it's an argument in cfg
            [] maybe get rid of click.x
    [] how would I build a model that gets arctic right?
        - linear model underestimates cooling in that area in ssp245
            - co2 from 10-20 y ago initiates greenland melt? 
      - > polynomial pattern scaling mostly get Arctic right. FairGP definitely does.

[] Download 3hr tas, huss, ps from esgf cnrm-esm2-1 for 2014-2100 for ssp585-over and 1 ensemble member.
    [] The 3 models for ssp585-over are not enough to avg out internal variability
    [] The 12 model for ssp127 should be enough.
    --> that goes beyond this emulator tutorial.

Archive && Done:
publish-ready:
    [x] Clean references
    [x] run whole notebook
    [x] ** did climatebench hold out historical AND ssp245 or just ssp245? ** I think I'm train and testing on historical data.
        -> historical is used in train and test in ClimateBench. I do the same.
    [x] rewrite intro to methods section: ML could be good. Here we first try Linear. 
        - Then find that polynomial can slightly improve. 
        - Point to exact file in climatebench notebook for ML model (if there's time implement local NN). 
        - Then say I don't implement NN because of internal variability overfitting 
        -> point to MPI data for 50 ensemble or temporal averaging paper.
    [x] clean table of contents
        restart and use "markdown all in one: create table of contents" command
    [x] how to integrate polynomial pattern scaling?
        [x] move complexity over performance into discussion
[x] clone explore_temperature for precip -> done.
[x] plot ch4, so2, and bc over time like climatebench fig1 
[x] plot all 740 training data samples. I want to know if I can learn as a human how to do the prediction task. 
    [] find out why 'tas' runs from -3 to +5? Am I plotting delta tas? But at which point have I dont the conversion.
    [] plot spatially-resolved 20year average tas on right and global co2 concentrations over time on left. The question is if I can see a mapping in between the co2 and local tas values?
[x] create scatterplot of co2 to each pixel? to see if co2 relates locally linearly to tas
    -> I plotted global T to local T for each pixel and I know that global co2 linearly correlates with global T
[x] create 2nd order polynomial fit instead of pattern scaling. I'm interested if there's good trends in the global T vs. local T plot.
    -> I plotted degree of polynomial fit over performance and found that 5th order polynomial fits the data best.
[] other model in-/output possibilities:
    [x] ClimateBench: map global cum. CO2 emissions + global CH4 emis. + spatially-resolved annual (SO2,BC) at time t to local T
        [] Linear: map annual cum. CO2 emission + (CH4,SO2,BC) emissions at time t linearly to global T at t. Then map global T + (SO2, BC) maps to local T maps
    [] Nat-Var-FCNN: map 10yr cum. co2 + (CH4, SO2, BC) time-series to 10 yr avg local T
    [] *Linear&FaiRGP: map annual cum. CO2 emission + (CH4,SO2,BC) emissions at time t linearly to global T at t. then map global T patterns to local T*
        [x] map co2 -> T
        [] *map co2, ch4, bc, so2 -> T* -- do I even need that because ch4,bc,so2 have such little impact on the global scale?
            - adding so2 might improve the 1960-2000 fit?
            - adding so2 might improve accuracy with held-out ssp370 in india&china
            - adding ch4, bc, so2 would allow en-roads integration?
[x] calculate NRMSE to compare with climatebench
[x] create a linear time difference model
    [] calculate tas(t)-tas(t-1) on smoothened data.
        Could I also smoothen the difference instead? I don't think so, it looks so noisy..
        Need to calculate difference using polynomial
        [] Fix the bug that timesteps dont seem to match
    [] drop duplicate time data in time-instant linear regression model
    [x] calculate inputs: time-difference vector tas(t) - tas(t-1)
    [x] calculate outputs: locally-resolved tas(t, xy)
        --> see why double check is wrong at some points.
    [] retrain patternscaling model for this in/output combination
        [x] write raw code to extend patternscaling code to multi-variate
        [x] text code extension for multi-variate linear patternscaling.
    [] evaluate if that gets the north atlantic cold blob right

[x] change colormap to discrete. Its super hard to read any values.
    [x] plot onto a little nicer projection
[x] use today's temperature as baseline.
[x] show 2100 temperature, not 2080-2100
[x] set tasmin and tasmax to be min,max plotted value.
[x] set co2min, max to be today's values
[x] add main
[x] check why model disagrees with baseline at 0.87°C
[x] create interactive demo
    [x] write model.predict() that takes global co2 and predicts global T
    [x] create xarray with dimensions: (co2 avg over 2080-2100), (global T avg over 2080-2100), (latitude), (longitude). 
    And values: (local T).
    [x] store or compute on the fly? -> storing is faster, but *on-the-fly* is cooler. -> compute on-the-fly
    [x] first, write model.predict() that takes global T and predicts local T
        - store linear regression coefficients from notebook.
    [x] create tas_global slider
    [x] query tas_local = model.predict(tas_global)
    [x] plot tas_local onto cartopy
    [x] host in web via streamlit
        [x] host as map -> streamlit-folium seems to buggy (https://folium.streamlit.app/) -> streamlit.map only does scatter plots -> just use cartopy for now
    [x] host in jupyter notebook via xarray bokeh -> too buggy
[x] plot (pred - baseline) surface temperature anomaly 
[x] host on external webpage
    [x] write requirements.txt that installs all dependencies
    [x] create dummy github. Find dummy email address that doesnt have a github -> using @climate-viz
    [x] debug streamlit build
        [x] streamlit needs climatebench data
            either download data files during build
            or reduce  data files. 
    ->>> accessible on https://climate-emulator-tutorial.streamlit.app/
[x] plot pixel wise frequency of TAS values
    - calculate running sum of histogram over all images TAS images
[x] plot tas histogram in test set
[x] In which regions does the linear pattern scaling break down?
    [x] create 2D map plot of (pattern scaling - ground-truth local tas) on the avg in 2080-2100.
    [x] plot error for 26 SREX regions (only land) or 58 AR6-WGI regions, e.g., Arctic, Monsoon region,  
        -> see tutorial of AR6-WGI at: https://github.com/SantanderMetGroup/ATLAS/blob/main/notebooks/reference-regions_Python.ipynb
    [x] plot regional grid according to notebook, [7], with label "abbrev", add_ocean=True
    [x] plot global T and local T over time in Arctic (then in Monsoon, etc.) -> done!
    * it seems like all errors - even in arctic - are just the result of internal variability?! * -> maybe, maybe not.
[x] download data locally to avoid google colab...
[x] declutter notebook by moving unet_model into python files
[x] declutter climate-emulator-tutorial notebook by moving normalize to python files
[x] declutter tutorial by moving autoregressive dataset into python files
[x] fit baseline global co2 -> global T -> local T using linear regression.
[x] map global cum. co2, ch4, bc, and so2 at t to global T at t
    reshape into list of data samples or large numpy array?
        numpy array easy for linear regression.
        list easy for fcnn data loader
        -> do a list and write linear regression to pull all data first.
        WHY IS THIS SO COMPLICATED?!
            i have multiple scenarios who's information i dont want to lose
            i have multiple timestamps who's information i dont want to lose.
            **i need to find a library for processing video data?**
[x] write extensible code for ghg -> cmip output mapping
    write it as dataset_utils: interim_to_processed.py
    inputs - batch, c, h, w
        e.g., global cum. co2, ch4, bc, so2 at t
        e.g., global cum. co2, ch4 and local bc, so2 at t
        (e.g., global cum. co2, ch4 over t-10:t and local bc, so2)
        e.g., global cum. co2, ch4, local bc, so2 at t and 
            local T, huss, ps at t-1
        e.g., global cum. co2, ch4, local bc, so2 at t and
            local T, huss, ps at t-3:t-1
    outputs - batch, c, h, w
        e.g., global T at t
        e.g., local T at t
        e.g., local T, huss, ps at t
        e.g., local T, huss , ps at t+3