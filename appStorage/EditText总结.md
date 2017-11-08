1、让光标显示在最后位置

    edt.setSelection(edt.getText().toString().trim().length());

2、让控件失去光标

   >让下一个控件获取焦点
   
    edt2.requestFocus();


3、监控输入字符

    edt.addTextChangedListener();

4、监控焦点

    edt.setOnFocusChangedListener();

5、约定行数

    android:lines = "1"
    android:maxLine="3"
    android:minLine="1"

