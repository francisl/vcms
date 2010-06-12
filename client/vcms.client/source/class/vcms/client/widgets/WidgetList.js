qx.Class.define("vcms.client.widgets.WidgetList",
{
    extend : qx.ui.container.Composite,
 
    construct : function()
    {
        this.base(arguments);
        
        this.setLayout(new qx.ui.layout.VBox().set({ spacing: 2 }));
        this.add(new qx.ui.form.List());
        var buttons_container = new qx.ui.container.Composite(new qx.ui.layout.HBox());
        buttons_container.add(new qx.ui.form.Button("Add widget to page"), {flex: 0});
        buttons_container.add(new qx.ui.core.Spacer(), {flex: 1});
        this.add(buttons_container);
    }
});

