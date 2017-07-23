class TemperaturePage extends PageView
{ 
	constructor(model)
	{
		super('temperature');
		this.initialize();
		//this._lights = new EventsDeviceListView(model.devices());
	}

	title()
	{
		return "TEMP";
	}

	icon_class()
	{
		return "glyphicon-scale";
	}

	
	initialize()
	{
		//local values 
		this.temp_kitchen_current = 22;
		this.temp_kitchen_preset = 20;
		this.temp_living_current = 24;
		this.temp_living_preset = 22;
		this.temp_hallway_current = 19;
		this.temp_hallway_preset = 18
		this.temp_bath_current = 21;
		this.temp_bath_preset = 23; 
		this.temp_bed_current = 22;
		this.temp_bed_preset = 20;
	}
		
	setup()
	{
		this.load_temp();
		this.setup_buttons();
	}
	
	load_temp()
	{
		//->local<- change of temperature with onclick / loading values on page load

		$('#temperature .kitchen    .current').html(this.temp_kitchen_current);
		$('#temperature .kitchen    .preset').html(this.temp_kitchen_preset);
		$('#temperature .kitchen    .add').on('click', () => 
			{
			this.temp_kitchen_current = this.temp_kitchen_current + 1;
			$('#temperature .kitchen    .current').html(this.temp_kitchen_current);
			});
		$('#temperature .kitchen    .sub').on('click', () => 
			{
			this.temp_kitchen_current = this.temp_kitchen_current - 1;
			$('#temperature .kitchen    .current').html(this.temp_kitchen_current);
			});
		
		$('#temperature .living    .current').html(this.temp_living_current);
		$('#temperature .living    .preset').html(this.temp_living_preset);
		$('#temperature .living    .add').on('click', () => 
			{
			this.temp_living_current = this.temp_living_current + 1;
			$('#temperature .living    .current').html(this.temp_living_current);
			});
		$('#temperature .living    .sub').on('click', () => 
			{
			this.temp_living_current = this.temp_living_current - 1;
			$('#temperature .living    .current').html(this.temp_living_current);
			});
		
		$('#temperature .hallway    .current').html(this.temp_hallway_current);
		$('#temperature .hallway    .preset').html(this.temp_hallway_preset);
		$('#temperature .hallway    .add').on('click', () => 
			{
			this.temp_hallway_current = this.temp_hallway_current + 1;
			$('#temperature .hallway    .current').html(this.temp_hallway_current);
			});
		$('#temperature .hallway    .sub').on('click', () => 
			{
			this.temp_hallway_current = this.temp_hallway_current - 1;
			$('#temperature .hallway    .current').html(this.temp_hallway_current);
			});
		
		$('#temperature .bath    .current').html(this.temp_bath_current);
		$('#temperature .bath    .preset').html(this.temp_bath_preset);
		$('#temperature .bath    .add').on('click', () => 
			{
			this.temp_bath_current = this.temp_bath_current + 1;
			$('#temperature .bath    .current').html(this.temp_bath_current);
			});
		$('#temperature .bath    .sub').on('click', () => 
			{
			this.temp_bath_current = this.temp_bath_current - 1;
			$('#temperature .bath    .current').html(this.temp_bath_current);
			});
		
		$('#temperature .bed    .current').html(this.temp_bed_current);
		$('#temperature .bed    .preset').html(this.temp_bed_preset);
		$('#temperature .bed    .add').on('click', () => 
			{
			this.temp_bed_current = this.temp_bed_current + 1;
			$('#temperature .bed    .current').html(this.temp_bed_current);
			});
		$('#temperature .bed    .sub').on('click', () => 
			{
			this.temp_bed_current = this.temp_bed_current - 1;
			$('#temperature .bed    .current').html(this.temp_bed_current);
			});
	}
	
	setup_buttons()
	{
		//show notification if a general button is pushed. Necessary because current temperature will not adjust immediately.  -jz
		$('#button_preset').on('click', () => 
			{
			var text_standby = "all devices are going to preset";
			$('#temperature .notification').html(text_standby);
			var c = "hidden";
			$('#temperature .button_notification').removeClass(c);
			});
		
		$('#button_standby').on('click', () => 
			{
			var text_standby = "all devices are going to standby";
			$('#temperature .notification').html(text_standby);
			var c = "hidden";
			$('#temperature .button_notification').removeClass(c);			});
		
		$('#button_turnoff').on('click', () => 
			{
			var text_standby = "all devices are getting turned-off";
			$('#temperature .notification').html(text_standby);
			var c = "hidden";
			$('#temperature .button_notification').removeClass(c);			});	
	}
	
	
	show()
	{
		//this._lights.show();
	}

	close()
	{
		//this._lights.close();
	}
} 
