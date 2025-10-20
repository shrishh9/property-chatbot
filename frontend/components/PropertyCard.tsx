import { Home, MapPin, Bath, Wind, Calendar } from 'lucide-react';

interface PropertyCardProps {
  property: {
    title: string;
    type: string;
    price: string;
    carpet_area: string;
    location: string;
    full_address: string;
    status: string;
    bathrooms: number | string;
    balcony: number;
    furnished: string;
    possession: string;
    slug: string;
    image?: string;
  };
}

export default function PropertyCard({ property }: PropertyCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-xl p-4 hover:shadow-lg transition-shadow">
      <div className="flex justify-between items-start mb-3">
        <div>
          <h3 className="text-lg font-bold text-gray-800">{property.title}</h3>
          <div className="flex items-center text-sm text-gray-600 mt-1">
            <MapPin size={14} className="mr-1" />
            <span>{property.location}</span>
          </div>
        </div>
        <div className="text-right">
          <p className="text-xl font-bold text-blue-600">{property.price}</p>
          <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
            {property.status}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 mb-3">
        <div className="flex items-center text-sm text-gray-600">
          <Home size={16} className="mr-2 text-gray-400" />
          <span>{property.type} • {property.carpet_area}</span>
        </div>
        <div className="flex items-center text-sm text-gray-600">
          <Bath size={16} className="mr-2 text-gray-400" />
          <span>{property.bathrooms} Bathrooms</span>
        </div>
        <div className="flex items-center text-sm text-gray-600">
          <Wind size={16} className="mr-2 text-gray-400" />
          <span>{property.balcony} Balcony</span>
        </div>
        <div className="flex items-center text-sm text-gray-600">
          <Calendar size={16} className="mr-2 text-gray-400" />
          <span>{property.furnished}</span>
        </div>
      </div>

      <div className="pt-3 border-t border-gray-100">
        <p className="text-xs text-gray-500 mb-2">{property.full_address}</p>
        <a
          href={`/project/${property.slug}`}
          className="text-sm text-blue-600 hover:text-blue-800 font-medium"
        >
          View Details →
        </a>
      </div>
    </div>
  );
}
