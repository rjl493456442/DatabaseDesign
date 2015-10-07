//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches

$(".next").click(function(){
  if(animating) return false;
  animating = true;

  current_fs = $(this).parent();
  next_fs = $(this).parent().next();

  //activate next step on progressbar using the index of next_fs
  $("#progressbar li").eq($("fieldset").index(next_fs)).addClass("active");

  //show the next fieldset
  next_fs.show();
  //hide the current fieldset with style
  current_fs.animate({opacity: 0}, {
    step: function(now, mx) {
      //as the opacity of current_fs reduces to 0 - stored in "now"
      //1. scale current_fs down to 80%
      scale = 1 - (1 - now) * 0.2;
      //2. bring next_fs from the right(50%)
      left = (now * 50)+"%";
      //3. increase opacity of next_fs to 1 as it moves in
      opacity = 1 - now;
      current_fs.css({'transform': 'scale('+scale+')'});
      next_fs.css({'left': left, 'opacity': opacity});
    },
    duration: 800,
    complete: function(){
      current_fs.hide();
      animating = false;
    },
    //this comes from the custom easing plugin
    easing: 'easeInOutBack'
  });
});

$(".previous").click(function(){
  if(animating) return false;
  animating = true;

  current_fs = $(this).parent();
  previous_fs = $(this).parent().prev();

  //de-activate current step on progressbar
  $("#progressbar li").eq($("fieldset").index(current_fs)).removeClass("active");

  //show the previous fieldset
  previous_fs.show();
  //hide the current fieldset with style
  current_fs.animate({opacity: 0}, {
    step: function(now, mx) {
      //as the opacity of current_fs reduces to 0 - stored in "now"
      //1. scale previous_fs from 80% to 100%
      scale = 0.8 + (1 - now) * 0.2;
      //2. take current_fs to the right(50%) - from 0%
      left = ((1-now) * 50)+"%";
      //3. increase opacity of previous_fs to 1 as it moves in
      opacity = 1 - now;
      current_fs.css({'left': left});
      previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
    },
    duration: 800,
    complete: function(){
      current_fs.hide();
      animating = false;
    },
    //this comes from the custom easing plugin
    easing: 'easeInOutBack'
  });
});
function validate_required(field, alerttext)
{
    with(field)
    {
        if(value == null || value == "")
        {
            alert(alerttext);
            return false;
        }
        else
        {
            return true;
        }
    }
}
function validate_password(field1, field2, alerttext)
{
    var pass;
    var passconfirm;
    with(field1)
    {
        pass = value;
    }
    with(field2)
    {
        passconfirm = value;
    }
    if(passconfirm != pass)
    {
        alert(alerttext);
        return false;
    }
    else
    {
        return true;
    }

}
function validate_email(field, alerttext)
{
    with(field)
    {
        apos=value.indexOf("@");
        dotpos=value.lastIndexOf(".");
        if (apos<1||dotpos-apos<2)
        {
            alert(alerttxt);
            return false;
        }
        else
        {
            return true;
        }
    }
}
function validate_form(thisform)
{
    with(thisform)
    {
        if(validate_required(email,"Email Must be filled Out!") ==  false)
        {
            email.focus();
            return false;
        }
        if(validate_required(username,"Username Must be filled Out!") ==  false)
        {
            username.focus();
            return false;
        }
        if(validate_required(pass,"Password Must be filled Out!") ==  false)
        {
            pass.focus();
            return false;
        }
        if(validate_required(cpass,"PasswordConfirm Must be filled Out!") ==  false)
        {
            cpass.focus();
            return false;
        }
        if(validate_required(province,"Province Must be filled Out!") ==  false)
        {
            province.focus();
            return false;
        }
        if(validate_required(weight,"weight Must be filled Out!") ==  false)
        {
            weight.focus();
            return false;
        }
        with(weight)
        {
            if(isNaN(value) || weight < 0)
            {
               alert("Invalid Weight input");
            }
        }
        with(height)
        {
            if(isNaN(value) || value < 100 ||value > 250)
            {
               alert("Invalid Height input");
            }
        }
        with(age)
        {
            if(isNaN(value) || value < 0 || value > 100)
            {
               alert("Invalid age input");
            }
        }
        if(validate_required(uname,"Personal Name Must be filled Out!") ==  false)
        {
            uname.focus();
            return false;
        }
        if(validate_required(age,"Age Must be filled Out!") ==  false)
        {
            age.focus();
            return false;
        }
        if(validate_required(sex,"Sex Must be filled Out!") ==  false)
        {
            sex.focus();
            return false;
        }
        if(validate_required(nationality,"Nationality Must be filled Out!") ==  false)
        {
            nationality.focus();
            return false;
        }
        if(validate_required(category,"Register Category Must be filled Out!") ==  false)
        {
            category.focus();
            return false;
        }
        if(validate_required(height,"Height Must be filled Out!") ==  false)
        {
            height.focus();
            return false;
        }
        if(validate_required(level,"Level Must be filled Out!") ==  false)
        {
            level.focus();
            return false;
        }

        if(validate_password(pass, cpass, "Password Must be same!") == false)
        {
            pass.focus();
            return false;
        }
        if(validate_email(email,"Invalid EmailAddress!") == false)
        {
            email.focus();
            return false;
        }
    }
}
