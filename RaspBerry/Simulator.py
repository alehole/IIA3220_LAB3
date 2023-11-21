class Simulator:
	def __init__(self, y_init, Ts):
		self.Tout = y_init
		self.e_k1 = 0
		self.Kh = 3.5
		self.theta_t = 22
		self.theta_d = 2
		self.Tenv = 21.5
		self.Ts = Ts
		self.Tout_prev = y_init
		
	def AirHeaterModel(self,CV):
		self.Tout_prev = self.Tout;
		self.Tout = self.Tout_prev + (self.Ts/self.theta_t) * (-self.Tout_prev + self.Kh*CV + self.Tenv);
		return self.Tout
		
