// Application: Vimba - CMS
// Copyright (c) 2010 Vimba inc. All rights reserved.
// Created by Francis Lavoie

var inputbox_manager = {
    last_input_value : ''
    , clear_input_on_focus : function (inputbox){
        this.last_input_value = inputbox.value;
        inputbox.value = ''; 
        }
    , reset_input_when_unfocus : function (inputbox){
        inputbox.value = this.last_input_value;
        }
}

