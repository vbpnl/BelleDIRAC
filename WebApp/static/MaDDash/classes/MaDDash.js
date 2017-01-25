Ext.define('BelleDIRAC.MaDDash.classes.MaDDash', {
  extend : 'Ext.dirac.core.Module',

  requires :
    ["Ext.dirac.utils.DiracToolButton", "Ext.dirac.utils.DiracGridPanel", "Ext.dirac.utils.DiracPagingToolbar",
     "Ext.dirac.utils.DiracApplicationContextMenu","Ext.dirac.utils.DiracBaseSelector","Ext.dirac.utils.DiracAjaxProxy"],
  

     dataFields : [ { name : 'Source'},{ name : 'Dest'},{ name : 'Average', type : 'float'}],


     initComponent : function() {

       var me = this;

       if (GLOBAL.VIEW_ID == "desktop") {

         me.launcher.title = "MaDDash";
         me.launcher.maximized = false;

         var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

         me.launcher.width = oDimensions[0];
         me.launcher.height = oDimensions[1] - GLOBAL.APP.MAIN_VIEW.taskbar.getHeight();

         me.launcher.x = 0;
         me.launcher.y = 0;

       }

       if (GLOBAL.VIEW_ID == "tabs") {

         me.launcher.title = "MaDDash";
         me.launcher.maximized = false;

         var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

         me.launcher.width = oDimensions[0];
         me.launcher.height = oDimensions[1] - GLOBAL.APP.MAIN_VIEW.taskbar.getHeight();

         me.launcher.x = 0;
         me.launcher.y = 0;

       }

       Ext.apply(me, {
         layout : 'border',
         bodyBorder : false,
         defaults : {
           collapsible : true,
           split : true
         }
       });

       me.callParent(arguments);

     },
     /**
      * It builds the widget.
      */
     buildUI : function() {

       var me = this;

      Ext.Ajax.request({
        url: GLOBAL.BASE_URL + 'MaDDash/getGrid',
        success: function(response){

        var img = Ext.create('Ext.Img', {
              region : "center",
              src : GLOBAL.BASE_URL + "static/BelleDIRAC/MaDDash/images/MaDDashMesh.png",
              maxHeight:850,
              maxWidth: 850
            });

        me.add([ img ])
        }
      });
    }

  });
