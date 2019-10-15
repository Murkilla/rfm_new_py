(function ($) {
    // let gaApiUrl = 'http://td.turingdigital.com.tw/get_ga_data';
    var gaAccountUrl = 'http://td.turingdigital.com.tw/get_ga_data/account_summary';
  
  
  
  
    $(function () {
      getAccountData();
    });
  
    function getAccountData() {
      //account_mail = $('body > div.top-menu > ul > li > a > span').text().trim()
      //var gaAccountUrl = 'https://asia-east2-max-td-project.cloudfunctions.net/function-1?key='+account_mail
      $.get(gaAccountUrl, function (data) {
        let items = data.items;
        let web_properties = items[0].web_properties;
        init_options(data);
        setAccountEvent(items, web_properties);
        // setEvent();
        console.log(gaAccountUrl)
        // 預設值
        // $('#item').val('15599013').change();
        // $('#web_property').val('UA-15599013-21').change();
        // $('#profile').val('56220486');
        $('#datetimepicker6 > input').val('2019-01-01');
        $('#datetimepicker7 > input').val('2019-05-01');
        // $("#data-compare-check").change();  // �凒�鰵鞈���
        // $('#time-compare').val('2018-10-01 ~ 2018-10-30');
        // $('#submit').click();
      }, 'json');
    }
  
    function setAccountEvent(items, web_properties) {
      $("#item").change(function () {
        let selected_item_id = $('#item :selected').val();
        let selected_item = search_obj_by_id(items, selected_item_id);
        web_properties = selected_item.web_properties;
        reset_web_property_options(web_properties);
      });
  
      $("#web_property").change(function () {
        let selected_web_property_id = $('#web_property :selected').val();
        let selected_web_property = search_obj_by_id(web_properties, selected_web_property_id);
        let profiles = selected_web_property.profiles;
        reset_profile_options(profiles);
      });
  
      // let item_id = "45833400";
      // let web_property_id = "UA-45833400-1";
      // let profile_id = "79190624";
  
      // $("#item [value='" + item_id + "']").prop('selected', true);
      // let selected_item = search_obj_by_id(items, item_id);
      // web_properties = selected_item.web_properties;
      // reset_web_property_options(web_properties);
  
      // $("#web_property [value='" + web_property_id + "']").prop('selected', true);
      // let selected_web_property = search_obj_by_id(web_properties, web_property_id);
      // let profiles = selected_web_property.profiles;
      // reset_profile_options(profiles);
  
      // $("#profile [value='" + profile_id + "']").prop('selected', true);
    }
  
    function init_options(account_summary) {
      let items = account_summary.items;
      reset_item_options(items);
    }
  
    function reset_item_options(items) {
      $("#item").empty();
      append_options("item", items);
  
      let selected_item_id = $('#item :selected').val();
      let selected_item = search_obj_by_id(items, selected_item_id);
      let web_properties = selected_item.web_properties;
      reset_web_property_options(web_properties);
    }
  
    function append_options(_id, objs) {
      objs.forEach(function (obj) {
        $("#" + _id).append("<option value=" + obj.id + ">" + obj.name + "</option>");
      });
    }
  
    function reset_web_property_options(web_properties) {
      // console.log('web_properties = ', web_properties);
      $("#web_property").empty();
      append_options("web_property", web_properties);
  
      let selected_web_property_id = $('#web_property :selected').val();
      let selected_web_property = search_obj_by_id(web_properties, selected_web_property_id);
      let profiles = selected_web_property.profiles;
      reset_profile_options(profiles);
    }
  
    function reset_profile_options(profiles) {
      $("#profile").empty()
      append_options("profile", profiles);
    }
  
    function search_obj_by_id(objs, _id) {
      for (let idx in objs)
        if (objs[idx].id == _id)
          return objs[idx];
    }
  
  
  })(jQuery)
  