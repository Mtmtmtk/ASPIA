export const contents = {
    Fourier:{
        sentences:[
            "Fourier Transform is a fundamental transformation formula of all the acoustic signal processing methods used in this app, which can extract the input signal's frequencies.",
            'For example, if the input signal is a mixed sine wave which contains 440 Hz (A4) and 660 Hz (E5), the result of the Fourier Transform shows the sharp peaks at 440 Hz and 660 Hz points and no power at the other frequencies.',
            'Then how can the Fourier Transform be calculated?',
            'The following formula is the definition of the Fourier Transform.',
            'The output of Fourier Transform may include an imaginary number.',
            'There are two ways to plot the strength of the output, amplitude spectrum and power spectrum.',
            'Amplitude spectrum |F(ω)| is the absolute value of the output, and power spectrum |F(ω)|<sup>2</sup> is the square of the amplitude spectrum.',
            "Now, let's calculate this formula with the input signal mentioned above.",
            'Open the following tab to see the calculation process.',
            'The input signal can be described as follows:',
            'Substituting f(t) to the definition of the Fourier Transform gets the following result.',
            'Fig. 2 is a power spectrum, which is the square of the absolute value of F(ω).',
            'Therefore, the power spectrum can be calculated as follows:',
            'Finally, Fig. 2 in the "What is Fourier Transform?" section is the plot of the equation above when T is 1 seconds.',
            'Have you got the same value as written in the tab?',
            'However, this is not what happens on the computer.',
            'The signal inputted in the computer is somewhat sampled as the computer cannot handle the continuous signal.',
            'Therefore, the Fourier Transform should also correspond with it. The discrete version of the Fourier Transform is called Discrete Fourier Transform (DFT), given by the following formula.',
            'In practice, Fast Fourier Transform (FFT), an algorithm for fast and efficient computation of the DFT, is executed in this app.',
            'The usages of FFT are written in the later sections, so please look at them.'
        ],
        formulas:[
            '$$ { F(\\omega) = \\int_{-\\infty}^{+\\infty}f(t)e^{-j\\omega t}dt}  $$ ',
            '$$ { f(t) =  \\begin{cases}\\sin{\\omega_{1}t} + \\sin{\\omega_{2}t} & (-T \\le t \\le +T )\\\\ 0 & \\mathrm{else}\\end{cases} } $$',
            '$$ { \\omega_{1} = 2\\pi\\cdot 440t, \\ \\omega_{2} = 2\\pi\\cdot 690t} $$',
            '$$ { \\begin{eqnarray} F(\\omega) &=& \\int_{-T}^{+T}(\\sin{\\omega_{1}t} + \\sin{\\omega_{2}t}) \\cdot e^{-j\\omega t}dt \\\\ &=& \\int_{-T}^{+T}(\\frac{e^{\\ j\\omega_{1}t}-e^{-j\\omega_{1}t}}{2j}+ \\frac{e^{\\ j\\omega_{2}t}-e^{-j\\omega_{2}t}}{2j})\\cdot e^{-j\\omega t}dt  \\\\ &=& \\frac{1}{2j}\\int_{-T}^{+T}(e^{\\ j(\\omega_{1} - \\omega)t}-e^{\\ j(-\\omega_{1}-\\omega)t} + e^{\\ j(\\omega_{2}-\\omega)t}-e^{\\ j(-\\omega_{2}-\\omega)t}) \\ dt  \\\\ &=& jT(\\frac{\\sin(\\omega_{1}+\\omega)}{\\omega_{1}+\\omega} - \\frac{\\sin(\\omega_{1}-\\omega)}{\\omega_{1}-\\omega} + \\frac{\\sin(\\omega_{2}+\\omega)}{\\omega_{2}+\\omega} + \\frac{\\sin(\\omega_{2}-\\omega)}{\\omega_{2}-\\omega})  \\end{eqnarray} }  $$ ',
            '$$ { |F(\\omega)| = T^2(\\frac{\\sin(\\omega_{1}+\\omega)}{\\omega_{1}+\\omega} - \\frac{\\sin(\\omega_{1}-\\omega)}{\\omega_{1}-\\omega} + \\frac{\\sin(\\omega_{2}+\\omega)}{\\omega_{2}+\\omega} + \\frac{\\sin(\\omega_{2}-\\omega)}{\\omega_{2}-\\omega})^2} $$',
            '$$ { F(k) = \\sum_{n=0}^{N-1}f[n]e^{-j\\frac{2\\pi k}{N} n} \\ \\ (k = 0,1,2,...,N-1)} $$'
        ],
        images: [
            { src: require('@/assets/theory/FFT_raw.jpg'),    caption: 'Raw Signal of A4 and E5' },
            { src: require('@/assets/theory/FFT_Result.jpg'), caption: 'The FFT result of Fig. 1' },
        ]
    },
    Spectrogram: {
        sentences: [
            'The spectrogram is a visualization of the input audio file so that the temporal changes such as pitch and power can be read simultaneously.',
            "Before getting into the spectrogram specification, let's remind of the Fourier Transform.",
            'Fourier Transform is the method to extract the frequency component of the entire section of the input signal.',
            "Then, don't you think if the spectrogram can be created by dividing the input signal into small time sections and executing the Fourier Transform to each of them?",
            'Yes, you are right.',
            'This method is Short-Time Fourier Transform (STFT), and the spectrogram is a visualization of the result of STFT.',
            'The formula of the STFT will be desribed in the next section.',
            'The formula of the STFT is a variant of the DFT formula; STFT requires dividing the input signal into small-time sections.',
            'However, dividing the signal is not simple; the window function should be applied as the Fourier Transform presupposes the input signal to be a periodic function (i.e. the simple division cannot assure the continuity).',
            'The solution is the window function, compensating for the discontinuity by making the beginning and end of the interval smaller.',
            'There are many types of window functions, and one of the most popular windows is the Hann window.',
            'The formula of the Hann window is as follows:',
            'It is possible to eliminate the discontinuity between the extracted signal by multiplying it with the window function.',
            'Therefore, the formula of the STFT can be expressed by using the hop size <i>R</i> and the current time index <i>m</i> as follows:',
            'The hop size is the difference between the window length <i>M</i> and the overlap length <i>L</i> given in Fig. 2.',
            'The overlap method is important in extracting the frequency response as much as possible.',
            'If the overlap percentage is zero, both ends of the frame cannot be extracted by the next/previous frame; it causes the frequency information to be missing at those parts.',
            'Therefore, applying the overlap compensates for the missing part of the signal by windowing partially in piles.'
        ],
        formulas: [
            '$$ { w[n] = 0.5 (1-\\cos{\\frac{2\\pi n}{N}}) } $$',
            '$$ { F(m, k) =  \\sum_{n=0}^{N-1}f[n]w[n-mR]e^{-j\\frac{2\\pi k}{N} n} \\ \\ (k = 0,1,2,...,N-1) } $$'
        ],
        images: [
            { src: require('@/assets/theory/spectrogramsource.png'), caption: 'The source sound of operatic voice' },
            { src: require('@/assets/theory/spectrogram.png'),       caption: 'The spectrogram of Fig.1' },
            { src: require('@/assets/theory/no_window.png'),         caption: 'The simple division without window function. Continuity has disappeared.' },
            { src: require('@/assets/theory/hann_window.jpg'),       caption: 'The graph of Hann window.' },
            { src: require('@/assets/theory/matlab_stft.png'),       caption: 'The outline of the STFT.' },
        ]
    },
    IrAnalysis: {
        sentences: [
            'In general, the impulse response is the response of the linear time-invariant system when the impulse signal <i>δ(t)</i>, given in the following equation, is input.',
            'This equation is an ideal signal; instead, the unit impulse signal, shown as follows, is used in practical terms.',
            'So, how does this response relate to acoustics?',
            'Surprisingly, the acoustic space can be approximated as a linear time-invariant system.',
            "If you don't understand the 'linear' and 'time-invariant', just know that the following equations can be applicable to the acoustic analysis (they are a bit complicated concepts).",
            'In acoustics, the impulse signal is an instantaneous burst.',
            "The hand clap and guns are examples, although they are not 'pure' impulse responses.",
            "But what does this 'pure' mean?",
            "First, let's look at their Fourier spectrums of them.",
            'As you can see, the spectrums of the hand clap and guns are unstable, whereas that of the unit signal is constant.',
            'The spectrum of the unit impulse signal shows that the signal has equal power across all frequency bands.',
            'The impulse response in acoustics is a recording of the direct sound and reverberation of this impulse signal emitted at a point in space, whose formula is written as follows:',
            'Moreover, the impulse response equals how much any frequency remains when the impulse signal is input.',
            'Therefore, analysing the impulse response reveals the characteristics of the recorded place.',
            'When analysing the impulse response, the Schroeder Curve is the critital factor for the evaluation.',
            'The definition of the Schroeder Curve is as follows:',
            'As you can see this equation, the Schroeder Curve is the energy decay curve, which describes the remaining energy at a time point <i>t</i>.',
            'The acoustic characteristics vary with frequency bands; therefore, it is necessary to filter the impulse response with certain frequency bands.',
            'In general, the impulse response is filtered with the octave bands, shown in Table 1.',
            'The specific method of filtering will be discussed in the last part of this section.',
            'There are five representive acoustic parameters (Reverberation time, Early decay time, C50, C80, and D50) that describes the character of the closed space.',
            'Expand the following panels to see what each parameter means.'
        ],
        formulas: [
            '$$ { \\delta (t) = \\begin{cases} \\infty & (t = 0) \\\\ 0 & \\mathrm{else} \\end{cases} } $$',
            '$$ { \\delta (t) = \\begin{cases} 1       & (t = 0) \\\\ 0 & \\mathrm{else} \\end{cases} } $$',
            '$$ { h(t) = \\int_{-\\infty}^{+\\infty}h(t-\\tau)\\delta (t)dt } $$',
            '$${ S(t) = {10 \\log_{10}{\\int_t^\\infty h^2(\\tau)d\\tau \\over \\int_0^\\infty h^2(\\tau)d\\tau}} }$$'
        ],
        images: [
            { src: require('@/assets/theory/unitIR_dB.jpg'),    caption: 'The power spectrum of the unit impulse signal.' },
            { src: require('@/assets/theory/hand_clap_ir.png'), caption: 'The power spectrum of the hand clap [1].' },
            { src: require('@/assets/theory/gun_ir.png'),       caption: 'The power spectrum of guns [2].' },
            { src: require('@/assets/theory/IR.gif'),           caption: 'The relationship between the impulse signal and impulse response.' },
            { src: require('@/assets/theory/Schroeder.png'),    caption: 'Example of the Schroeder curve.' },
        ]
    },
    Auralisation: {
        sentences: [
            'Auralisation is a method of creating an acoustic virtual reality; it is possible to reproduce a reverberant sound as if the sound source is played in an arbitrary space.',
            "Let's look at an example - the following sound file is an operatic voice recorded in the anechoic chamber.",
            'Now, prepare the impulse response. This time, the Usina del Arte concert hall is prepared.',
            'After the process, you get the operatic voice virtually sung in the concert hall!',
            'So how to create this kind of auralised sound file? In this app, what you should do is just to follow the instruction in the "Auralisation" section.',
            'The formula and its actual process are described in the next section.',
            'Auralisation, in other words, is a process realized by adding a resonance component (i.e. spatial impulse response) to each sample of the original anechoic signal.',
            'This operation is called convolution, widely used in many academic fields such as image processing, acoustics, and electronics.',
            'The formula of convolution can be defined as follows:',
            'where <i>h(t)</i> is an impulse response and <i>x(t)</i> is an input signal.',
            'Applying this formula directly in this app to create auralised sounds is possible.',
            'However, this equation takes a long time to calculate - the server may crash due to the amount of calculation if the long sound file is input.',
            'Therefore, this app embeds the auralisation section with the modified version of convolution, which uses the Fourier transform.',
            'The convolution in the time domain is the same as the multiplication in the frequency domain.',
            'The following conversion shows the relationship between the Fourier transform and the convolution.',
            'Thus, the auralisation can also be achieved by the following steps:',
            'This is what the system of this app does in the auralisation section.',
            'The FFT-modified convolution method calculates way faster than the standard convolution; it reduces the computation complexity from <i>O(n<sup>2</sup>)</i> to <i>O(n</i> log<i>(n))</i>[1].'
        ],
        formulas: [
            '$$ { \\begin{eqnarray} y(t) &=& \\int_{-\\infty}^{\\infty}h(t-\\tau)x(\\tau)d\\tau \\\\ &=& h(t) * x(t)\\end{eqnarray} } $$',
            '$$ { \\begin{eqnarray} F(y(t)) &=& F(h(t) * x(t)) \\\\  &=& \\int_{-\\infty}^{\\infty}(\\int_{-\\infty}^{\\infty}h(t-\\tau)x(\\tau)d\\tau)e^{-j\\omega t}dt \\\\ &=&  \\int_{-\\infty}^{\\infty}x(\\tau) (\\int_{-\\infty}^{\\infty}h(t-\\tau)e^{-j\\omega t}dt) d\\tau \\\\ &=&  \\int_{-\\infty}^{\\infty}x(\\tau) (\\int_{-\\infty}^{\\infty}h(t-\\tau)e^{-j\\omega (t-\\tau)} dt) e^{-j\\omega \\tau}d\\tau \\\\ &=&  \\int_{-\\infty}^{\\infty}x(\\tau) e^{-j\\omega \\tau}d\\tau \\  F(h(t)) \\\\ &=& F(x(t)) \\  F(h(t)) \\end{eqnarray} } $$'
        ],
        images: [
            { src: require('../../../assets/theory/convolution.gif'),    caption: 'The sample gif of the convolution image.' },
        ],
        audios: [
            { src: require('@/assets/theory/singing.wav'),          title: 'Anechoic Operatic Voice' },
            { src: require('@/assets/theory/usina_main_s1_p1.wav'), title: 'The impulse response of Usina del Arte concert hall, Spain' },
            { src: require('@/assets/theory/convoluted.wav'),       title: 'Auralised Operatic Voice' },
        ],
    }
    //WhatIsConvolution:{
    //    sentences:[
    //        'Convolution is the method of calculation, whose definition can be expressed by the following equation.',
    //        'This calculation means that the output is a binary operation in which a function g(t) is superimposed on a function f(t) while moving in parallel.',
    //        'However, this equation is converted into the discrete-time calculation in a computer as the computer cannot calculate the continuous functions.',
    //        'This app is using Fast Fourier Transform (FFT) instead of this equation, as the calculation time of the convolution is much longer than FFT.',
    //        'FFT is defined as the follwing equation, and its muplication in the Fourier dimension is as same as the convolution in the time domain.'
    //    ],
    //    formulas:[
    //        '$$ {(f \\ast g)(t) = \\int f(\\tau)g(t-\\tau)d\\tau}$$ ',
    //        '$$ {(f \\ast g)[n] = \\sum_{k=-\\infty}^\\infty f[k]g[n-k] }$$',
    //        '$$ {F[f(t)] = \\int f(t)e^{-j\\omega t} dt}$$',
    //        '$$ {\\begin{eqnarray} F[(f \\ast g)(t)] &=& \\int\\int f(\\tau)g(t-\\tau)d\\tau e^{-j\\omega t}dt \\\\ &=& \\int f(\\tau)\\int g(t-\\tau) e^{-j\\omega t}dt d\\tau8 \\\\ &=& \\int f(\\tau)e^{-j\\omega \\tau} d\\tau \\int g(t-\\tau) e^{-j\\omega (t-\\tau)}dt \\\\ &=& F[f(t)]F[g(t)]\\end{eqnarray}}$$',
    //    ],
    //    images:[
    //        require('@/assets/theory/convolution.gif')
    //    ]
    //},
    //SoundConvolution:{
    //    sentences:[
    //        'When analysing the impulse response, the Schroeder Curve is the '
    //    ],
    //    formulas:[],
    //    images:[],
    //},
}
