Ext.define('DIRAC.Belle2MaDDash.classes.Belle2MaDDash', {
  extend : 'Ext.dirac.core.Module',

  requires :
    ["Ext.dirac.utils.DiracToolButton", "Ext.dirac.utils.DiracGridPanel", "Ext.dirac.utils.DiracPagingToolbar",
     "Ext.dirac.utils.DiracApplicationContextMenu","Ext.dirac.utils.DiracBaseSelector","Ext.dirac.utils.DiracAjaxProxy"],
  
     /***
      * @param{Object} data
      * It loads the data from the User Profile to the widget.
      */
     // loadState : function(data) {

     //   var me = this;

     //   //loads the saved data related to the Grid Panel
     //   me.grid.loadState(data);

     //   //it loads the selector data
     //   //me.leftPanel.loadState(data);


     //   //it loads the selector panel status.
     //   //if (data.leftPanelCollapsed) {

     //     //if (data.leftPanelCollapsed)
     //       //me.leftPanel.collapse();

     //   //}
     // },
     // *
     //  * @return{Object}
     //  * It returns the data which will be saved in the User Profile.
      
     // getStateData : function() {

     //   var me = this;
     //   var oReturn = {};

     //   // data for grid columns
     //   oReturn.grid = me.grid.getStateData();
     //   // show/hide for selectors and their selected data (including NOT
     //   // button)
     //   //oReturn.leftMenu = me.leftPanel.getStateData();

     //   //oReturn.leftPanelCollapsed = me.leftPanel.collapsed;

     //   return oReturn;

     // },
     dataFields : [ { name : 'Source'},{ name : 'Dest'},{ name : 'Average', type : 'float'}],


     initComponent : function() {

       var me = this;

       if (GLOBAL.VIEW_ID == "desktop") {

         me.launcher.title = "Belle2MaDDash";
         me.launcher.maximized = false;

         var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

         me.launcher.width = oDimensions[0];
         me.launcher.height = oDimensions[1] - GLOBAL.APP.MAIN_VIEW.taskbar.getHeight();

         me.launcher.x = 0;
         me.launcher.y = 0;

       }

       if (GLOBAL.VIEW_ID == "tabs") {

         me.launcher.title = "Belle2MaDDash";
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
      * It build the widget.
      */
     buildUI : function() {

       var me = this;

      // Ext.Ajax.request({
      //   url: GLOBAL.BASE_URL + 'Belle2MaDDash/getGrid',
      //   success: function(response){
      //   // var container = Ext.create('Ext.container.Container', {
      //   //   layout: {
      //   //     type: 'hbox'
      //   //   },
      //   //   width: 1000,
      //   //   height: 1000,
      //   //   renderTo: Ext.getBody()

      //   // });
      //   var img = Ext.create('Ext.Img', {
      //         region : "center",
      //         src : GLOBAL.BASE_URL + "static/DIRAC/Belle2MaDDash/images/Belle2MaDDashMesh.png",
      //         maxHeight:850,
      //         maxWidth: 850
      //       });
      //   me.add([ img ])
        //me.add([ container ]);
        // var img = document.createElement("img");
        // img.src = GLOBAL.BASE_URL + 'static/DIRAC/Belle2MaDDash/images/Belle2MaDDashMesh.png'
        // //img.src = "/opt/dirac/pro/WebAppDIRAC/WebApp/static/DIRAC/Belle2MaDDash/images/Belle2MaDDashMesh.png";
        // //img.width = 10;
        // //img.height = 10;
        // img.alt = "Belle 2 MaDDash Mesh";

        // // This next line will just add it to the <body> tag
        // var div = document.createElement("div");
        // document.body.appendChild(div);
        // div.appendChild(img);
        //document.body.appendChild(img);
    //     }
    //   });
    // }

       /*
        * -----------------------------------------------------------------------------------------------------------
        * DEFINITION OF THE LEFT PANEL
        * -----------------------------------------------------------------------------------------------------------
        */

       // var selectors = {
       //     firstName : "First Name",
       //     lastName : "Last Name"
       // };

       // var textFields = {
       //     'ids' : "PersonalId"
       // }

       // var map = [ [ "firstName", "firstName" ], [ "lastName", "lastName" ]];

       // me.leftPanel = Ext.create('Ext.dirac.utils.DiracBaseSelector',{
       //   scope : me,
       //   cmbSelectors : selectors,
       //   textFields : textFields,
       //   datamap : map,
       //   url : "ExampleApp/getSelectionData"
       // });

       /*
        * -----------------------------------------------------------------------------------------------------------
        * DEFINITION OF THE GRID
        * -----------------------------------------------------------------------------------------------------------
        */

       var oProxy = Ext.create('Ext.dirac.utils.DiracAjaxProxy',{
         url : GLOBAL.BASE_URL + 'Belle2MaDDash/getChannelData'
       });

      me.dataStore = new Ext.data.JsonStore({

          proxy : {
              type : 'ajax',
              url : GLOBAL.BASE_URL + 'Belle2MaDDash/getChannelData',
              reader : {
                  type : 'json',
                  root : 'result'
              },
              timeout : 1800000
          },
          fields : [{ name : 'Source'}, 
                    { name : 'Dest'},
                    { name : 'Average', type : 'float'}
                    ],
          autoLoad : true

      });

       // var pagingToolbar = {};

       // var toolButtons = {
       //     'Visible':[
       //                {"text":"", "handler":me.__executeAction, "arguments":["example", ""],"properties":{tooltip : "Example", iconCls : "dirac-icon-reschedule"}}
       //                ]
       // };

       // pagingToolbar = Ext.create("Ext.dirac.utils.DiracPagingToolbar",{
       //   toolButtons : toolButtons,
       //   store : me.dataStore,
       //   scope : me
       // });

       var oColumns = {
           "Source" : {"dataIndex" : "Source"},
           "Dest" : {"dataIndex" : "Dest"},
           "Average" : {"dataIndex" : "Average"}
       };


       // var menuitems = {
       //     'Visible':[
       //                {"text":"Get info", "handler":me.__executeAction, "arguments":["Get info"], "properties":{tooltip:'Click to show....'}}
       //                ]};

       // me.contextGridMenu = new Ext.dirac.utils.DiracApplicationContextMenu({menu:menuitems,scope:me});

       me.grid = Ext.create('Ext.dirac.utils.DiracGridPanel', {
         store : me.dataStore,
         oColumns : oColumns,
         //contextMenu : me.contextGridMenu,
         //pagingToolbar : pagingToolbar,
         scope : me
       });
       
       //me.leftPanel.setGrid(me.grid);
       
     //   me.add([ me.grid ]);
     // }
     // __executeAction : function(action){
     //   var me = this;
     //   GLOBAL.APP.CF.alert(action+" button pressed","info");
     // }
   }
  });
