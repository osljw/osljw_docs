

列表
```
<select name='key_value' multiple="multiple" ONCHANGE="document.getElementById('relation').src = this.options[this.selectedIndex].value">
% for key_value in key_values:
    <option value={{key_value}}> {{key_value}} </option>
% end
</select>

<iframe name="iframe" id="relation" src={{src}} width="800" height="600">
</iframe>
```