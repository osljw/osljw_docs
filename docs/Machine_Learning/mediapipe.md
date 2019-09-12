
# mediapipe

- calculator
    - GetContract() 
        - 图初始化时，packet的类型确认
        - 静态函数 static ::MediaPipe::Status GetContract(CalculatorContract* cc)
    - Open()
        - 初始化caculator
        - virtual ::MediaPipe::Status Open(CalculatorContext* cc)
    - Process()
        - 
        - virtual ::MediaPipe::Status Process(CalculatorContext* cc) = 0
    - Close()
        - virtual ::MediaPipe::Status Close(CalculatorContext* cc)