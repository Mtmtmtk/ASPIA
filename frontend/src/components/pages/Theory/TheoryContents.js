export const contents = {
    WhatIsConvolution:{
        sentences:[
            'Convolution is the method of calculation, whose definition can be expressed by the following equation.',
            'This calculation means that the output is a binary operation in which a function g(t) is superimposed on a function f(t) while moving in parallel.',
            'However, this equation is converted into the discrete-time calculation in a computer as the computer cannot calculate the continuous functions.',
            'This app is using Fast Fourier Transform (FFT) instead of this equation, as the calculation time of the convolution is much longer than FFT.',
            'FFT is defined as the follwing equation, and its muplication in the Fourier dimension is as same as the convolution in the time domain.'
        ],
        formulas:[
            '$$ {(f \\ast g)(t) = \\int f(\\tau)g(t-\\tau)d\\tau}$$ ',
            '$$ {(f \\ast g)[n] = \\sum_{k=-\\infty}^\\infty f[k]g[n-k] }$$',
            '$$ {F[f(t)] = \\int f(t)e^{-j\\omega t} dt}$$',
            '$$ {\\begin{eqnarray} F[(f \\ast g)(t)] &=& \\int\\int f(\\tau)g(t-\\tau)d\\tau e^{-j\\omega t}dt \\\\ &=& \\int f(\\tau)\\int g(t-\\tau) e^{-j\\omega t}dt d\\tau8 \\\\ &=& \\int f(\\tau)e^{-j\\omega \\tau} d\\tau \\int g(t-\\tau) e^{-j\\omega (t-\\tau)}dt \\\\ &=& F[f(t)]F[g(t)]\\end{eqnarray}}$$',
        ],
        images:[
            require('@/assets/theory/convolution.gif')
        ]
    },
    ImpulseResponse:{
        sentences:[
            'The impulse response(IR) is an output signal of the convolution substituting the impulse signal for an input signal.',
            'The impulse signal can be expressed by the following equation.',
            "The impulse signal contains equal power at all frequencies, therefore, playing the implse signal in the closed space describes how the reveberation attenuates (which is a character of the space).",
            'Theoretically, this closed space is one of the discrete systems that takes x[n] as an input and creates an output y[n].',
            'T means an time-invariant linear discrete system.',
            'x[n] can be expressed by:',
            'Substituting T for the equation obtains the following process.',
            'Here, by replacing T[δ[n-k]] to h[n-k], you can obtain the following equation.',
            'As you can see, h[n] is the output of the system T inputting the impulse signal, and y[n] is a convolution of an input signal x[n] and the inpulse response h[n-k].',
            'As mentoined, the IR describes a character of a space, and it can be evaluated by the several acoustic parameters.',
            'These parameters are described in the IR Analysis section.',
        ],
        formulas:[
            '$${\\delta[n] = \\begin{cases} \\infty, \\mathrm{n=0} \\\\ 0, \\mathrm{n \\neq 0} \\end{cases}}$$',
            '$${y[n] = T[x[n]]}$$',
            '$${x[n] = \\sum_{k}x[k]\\delta[n-k]}$$',
            '$${\\begin{eqnarray} T[x[n]] &=& T[\\sum_{k}x[k]\\delta[n-k]] \\\\ &=& \\sum_{k}x[k]T[\\delta[n-k]]\\end{eqnarray}}$$',
            '$${y[n] = \\sum_{k}x[k]h[n-k]}$$',
        ],
        images:[
            require('@/assets/theory/IR.gif')
        ]
    },
    SoundConvolution:{
        sentences:[
            'When analysing the impulse response, the Schroeder Curve is the '
        ],
        formulas:[],
        images:[],
    },
    IrAnalysis:{
        sentences:[
            'When analysing the impulse response, the Schroeder Curve is the critital factor for the evaluation.',
            'The definition of the Schroeder Curve is as follows:',
            'As you can see this equation, the Schroeder Curve is the energy decay curve, which describes the remaining energy at a time point t.',
            'The evaluation is mostly executed with every octave band (See Fig.1).',
            'There are five representive acoustic parameters (Reverberation time, Early decay time, C50, C80, and D50) that describes the character of the closed space.',
            'Expand the following panels to see what each parameter means.'
        ],
        formulas:[
            '$${ S(t) = {10 \\log_{10}{\\int_t^\\infty h^2(t)dt \\over \\int_0^\\infty h^2(t)dt}} \\ \\mathrm{dB}}$$'
        ],
        images:[],
    }
}
