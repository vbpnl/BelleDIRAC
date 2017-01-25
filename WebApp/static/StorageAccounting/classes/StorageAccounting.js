Ext.define('BelleDIRAC.StorageAccounting.classes.StorageAccounting', {
  extend : 'Ext.dirac.core.Module',



     initComponent : function() {

       var me = this;

       if (GLOBAL.VIEW_ID == "desktop") {

         me.launcher.title = "Storage Accounting";
         me.launcher.maximized = false;

         var oDimensions = GLOBAL.APP.MAIN_VIEW.getViewMainDimensions();

         me.launcher.width = oDimensions[0];
         me.launcher.height = oDimensions[1] - GLOBAL.APP.MAIN_VIEW.taskbar.getHeight();

         me.launcher.x = 0;
         me.launcher.y = 0;

       }

       if (GLOBAL.VIEW_ID == "tabs") {

         me.launcher.title = "Storage Accounting";
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
        * DEFINITION OF THE LEFT PANEL
        * -----------------------------------------------------------------------------------------------------------
        */

        me.leftPanel = new Ext.create('Ext.panel.Panel', {
              region : "west",
              floatable : false,
              header : false,
              margins : '0',
              width : 375,
              minWidth : 330,
              maxWidth : 450,
              bodyPadding : 5,
              layout : 'anchor',
              autoScroll : true
            });
       
        var oPanelButtons = new Ext.create('Ext.toolbar.Toolbar', {
              dock : 'bottom',
              layout : {
                pack : 'center'
              },
              items : []
            });

        me.btnSubmit = new Ext.Button({

              text : 'Submit',
              margin : 3,
              iconCls : "dirac-icon-submit",
              listeners: {
              'click' : function() {
                  me.rightPanel.setLoading(true);
                  //me.rightPanel.remove([ me.plotImg ]);
                  var fileName = '';
                  var availableOrPledged = '';
                  var percentageOfTotalBool = false;
                  var percentageFullBool = false;
                  switch(me.combo.getValue()) {
                    case 'Available Storage in TB':
                      availableOrPledged = 'available';
                      fileName = 'availableStoragePie.png';
                      break;
                    case 'Pledged Storage in TB':
                      availableOrPledged = 'pledged';
                      fileName = 'pledgedStoragePie.png';
                      break;
                    case 'Available Storage as Percentage of Total':
                      availableOrPledged = 'available';
                      fileName = 'availableStoragePercentagePie.png';
                      percentageOfTotalBool = true;
                      break;
                    case 'Pledged Storage as Percentage of Total':
                      availableOrPledged = 'pledged';
                      fileName = 'pledgedStoragePercentagePie.png';
                      percentageOfTotalBool = true;
                      break;
                    case 'Percent Storage Site Full':
                      percentageFullBool = true;
                      fileName = 'percentFullPie.png';
                      break;

                  }
                  Ext.Ajax.request({
                    url: GLOBAL.BASE_URL + 'StorageAccounting/getStorage',
                    params: {
                      availableOrPledged: availableOrPledged,
                      percentageOfTotalBool: percentageOfTotalBool,
                      percentageFullBool: percentageFullBool
                    },
                    success: function(response){
                    //var me = this;
                      me.plotImg = Ext.create('Ext.Img', {
                            region : "center",
                            src : GLOBAL.BASE_URL + "static/BelleDIRAC/StorageAccounting/images/" + fileName,
                            listeners : {

                              render : function(oElem, eOpts) {
                                oElem.el.on({
                                      load : function(evt, ele, opts) {

                                        oElem.originalWidth = oElem.getWidth();
                                        oElem.originalHeight = oElem.getHeight();

                                        //me.__oprResizeImageAccordingToContainer();

                                      }
                                });

                              }
                            }
                      });

                      me.rightPanel.add([ me.plotImg ]);
                      me.rightPanel.setLoading(false);
                      //me.rightPanel.body.dom.innerHTML = response.responseText;
                      
                  //});
                }
                
          });
              }
            },
              scope : me

            });
        
        oPanelButtons.add(me.btnSubmit);
        me.leftPanel.addDocked(oPanelButtons);


      me.combo = Ext.create('Ext.form.field.ComboBox', { 
          store: ['Available Storage in TB', 'Pledged Storage in TB', 
          'Available Storage as Percentage of Total', 'Pledged Storage as Percentage of Total', 
          'Percent Storage Site Full'],
          width: 350,
          fieldLabel: 'Plot Type',
          editable: false,
          value: 'Available Storage in TB'
  });

      me.leftPanel.add([me.combo]);


       /*
        * -----------------------------------------------------------------------------------------------------------
        * DEFINITION OF THE RIGHT PANEL
        * -----------------------------------------------------------------------------------------------------------
        */

        me.rightPanel = new Ext.create('Ext.panel.Panel', {
              region : "center",
              floatable : false,
              header : false,
              margins : '0',
              bodyPadding : 0,
              layout : "absolute"
            });

       me.add([ me.leftPanel, me.rightPanel ]);
       me.btnSubmit.fireEvent('click', me.btnSubmit);
     }
});
