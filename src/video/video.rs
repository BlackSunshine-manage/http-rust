use crate::has_name::has_name;

pub struct Video { 
    pub name: String
}

impl has_name for Video {
    fn new(name: String) -> Self {
        Video {name}
    }

    fn name(&self) -> &str {
        &self.name
    }
}