define("ace/theme/dawn",["require","exports","module","ace/lib/dom"],function(a,b,c){b.isDark=!1,b.cssClass="ace-dawn",b.cssText=".ace-dawn .ace_editor {  border: 2px solid rgb(159, 159, 159);}.ace-dawn .ace_editor.ace_focus {  border: 2px solid #327fbd;}.ace-dawn .ace_gutter {  background: #e8e8e8;  color: #333;}.ace-dawn .ace_print_margin {  width: 1px;  background: #e8e8e8;}.ace-dawn .ace_scroller {  background-color: #F9F9F9;}.ace-dawn .ace_text-layer {  cursor: text;  color: #080808;}.ace-dawn .ace_cursor {  border-left: 2px solid #000000;}.ace-dawn .ace_cursor.ace_overwrite {  border-left: 0px;  border-bottom: 1px solid #000000;} .ace-dawn .ace_marker-layer .ace_selection {  background: rgba(39, 95, 255, 0.30);}.ace-dawn .ace_marker-layer .ace_step {  background: rgb(198, 219, 174);}.ace-dawn .ace_marker-layer .ace_bracket {  margin: -1px 0 0 -1px;  border: 1px solid rgba(75, 75, 126, 0.50);}.ace-dawn .ace_marker-layer .ace_active_line {  background: rgba(36, 99, 180, 0.12);}.ace-dawn .ace_marker-layer .ace_selected_word {  border: 1px solid rgba(39, 95, 255, 0.30);}       .ace-dawn .ace_invisible {  color: rgba(75, 75, 126, 0.50);}.ace-dawn .ace_keyword {  color:#794938;}.ace-dawn .ace_constant {  color:#811F24;}.ace-dawn .ace_invalid.ace_illegal {  text-decoration:underline;font-style:italic;color:#F8F8F8;background-color:#B52A1D;}.ace-dawn .ace_invalid.ace_deprecated {  text-decoration:underline;font-style:italic;color:#B52A1D;}.ace-dawn .ace_support {  color:#691C97;}.ace-dawn .ace_fold {    background-color: #794938;    border-color: #080808;}.ace-dawn .ace_support.ace_function {  color:#693A17;}.ace-dawn .ace_string {  color:#0B6125;}.ace-dawn .ace_string.ace_regexp {  color:#CF5628;}.ace-dawn .ace_comment {  font-style:italic;color:#5A525F;}.ace-dawn .ace_variable {  color:#234A97;}.ace-dawn .ace_markup.ace_underline {    text-decoration:underline;}.ace-dawn .ace_markup.ace_heading {  color:#19356D;}.ace-dawn .ace_markup.ace_list {  color:#693A17;}";var d=a("../lib/dom");d.importCssString(b.cssText,b.cssClass)})