Ext.define('BelleDIRAC.StorageHealth.classes.StorageHealth', {
  extend : 'Ext.dirac.core.Module',

  requires :
    ["Ext.dirac.utils.DiracGridPanel", "Ext.dirac.utils.DiracAjaxProxy"],
  

     initComponent : function() {

       var me = this;

       if (GLOBAL.VIEW_ID == "desktop") {

         me.launcher.title = "Storage Health";
         me.launcher.maximized = false;

         var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

         me.launcher.width = oDimensions[0];
         me.launcher.height = oDimensions[1] - GLOBAL.APP.MAIN_VIEW.taskbar.getHeight();

         me.launcher.x = 0;
         me.launcher.y = 0;

       }

       if (GLOBAL.VIEW_ID == "tabs") {

         me.launcher.title = "Storage Health";
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

     buildUI : function() {

       var me = this;

       /*
        * -----------------------------------------------------------------------------------------------------------
        * DEFINITION OF THE GRID
        * -----------------------------------------------------------------------------------------------------------
        */

       var oProxy = Ext.create('Ext.dirac.utils.DiracAjaxProxy',{
         url : GLOBAL.BASE_URL + 'StorageHealth/getStorageHealth'
       });

      me.dataStore = new Ext.data.JsonStore({

          proxy : {
              type : 'ajax',
              url : GLOBAL.BASE_URL + 'StorageHealth/getStorageHealth',
              reader : {
                  type : 'json',
                  root : 'result'
              },
              timeout : 1800000
          },
          fields : [{ name : 'StorageElement' }, 
                    { name : 'isLS' },
                    { name : 'isUP' },
                    { name : 'isDN' },
                    { name : 'isRMDIR' },
                    { name : 'isRM' },
                    { name : 'isHealthy' }
                    ],
          autoLoad : true

      });

       var oColumns = {
           "Storage Element" : {"dataIndex" : "StorageElement"},
           "isHealthy" : {"dataIndex" : "isHealthy",
                renderer : function(val, metaData, record) {
                    if (val) {
                        metaData.tdAttr = 'style="background-color: #99D699"';
                        return '<span style=' +
                        '"background: green;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }else {
                        metaData.tdAttr = 'style="background-color: #FF8080"';
                        return '<span style=' +
                        '"background: red;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }
                }
         },
           "isLS" : {"dataIndex" : "isLS", "width" : "5px",
                renderer : function(val) {
                    if (val) {
                        return '<span style=' +
                        '"background: green;' +
                        'display: block;' +
                        'width: 30px;' +  
                        'height: 30px;' +
                        'border-radius: 50%;' +
                        'margin-right: auto;' +
                        'margin-left: auto;">' +
                        '</span>';
                    }else {
                        return '<span style=' +
                        '"background: red;' +
                        'display: block;' +
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }
                }
         },
           "isUP" : {"dataIndex" : "isUP", "width" : "5px",
                renderer : function(val) {
                    if (val) {
                        return '<span style=' +
                        '"background: green;' + 
                        'display: block;' +  
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }else {
                        return '<span style=' +
                        '"background: red;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }
                }
         },
           "isDN" : {"dataIndex" : "isDN", "width" : "5px",
                renderer : function(val) {
                    if (val) {
                        return '<span style=' +
                        '"background: green;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }else {
                        return '<span style=' +
                        '"background: red;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' +
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }
                }
         },
           "isRMDIR" : {"dataIndex" : "isRMDIR", "width" : "5px",
                renderer : function(val) {
                    if (val) {
                        return '<span style=' +
                        '"background: green;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }else {
                        return '<span style=' +
                        '"background: red;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' +
                        'margin-left: auto;">' +
                        '</span>';
                    }
                }
         },
           "isRM" : {"dataIndex" : "isRM", "width" : "5px",
                renderer : function(val) {
                    if (val) {
                        return '<span style=' +
                        '"background: green;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }else {
                        return '<span style=' +
                        '"background: red;' + 
                        'display: block;' + 
                        'width: 30px;' + 
                        'height: 30px;' + 
                        'border-radius: 50%;' + 
                        'margin-right: auto;' + 
                        'margin-left: auto;">' +
                        '</span>';
                    }
                }
         }
       };


       me.grid = Ext.create('Ext.dirac.utils.DiracGridPanel', {
         store : me.dataStore,
         oColumns : oColumns,
         columnLines : true,
         scope : me
       });
    me.add([ me.grid ])   
   }
  });
